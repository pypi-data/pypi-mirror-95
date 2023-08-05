from contextvars import ContextVar
from datetime import datetime
from functools import wraps
from json import dumps, loads
from logging import getLogger
from time import monotonic
from typing import List, Optional, Union, Any, Dict, Mapping, Collection, Tuple

from databases import Database
from pydantic.main import BaseModel

from binp.db import ensure
from binp.events import Emitter

"""
Current journal record ID. Can be used only from functions under @journal.log decorators.
Useful to link some other entities to the journal record.
It's not recommended modify the variable outside core module.
"""
current_journal: ContextVar[Optional[int]] = ContextVar('current_journal', default=None)


class Record(BaseModel):
    """
    Single record in journal
    """
    #: message provided by invoker
    message: str
    #: record creation time
    created_at: datetime
    #: fields defined for record
    params: Dict[str, Any]


class Headline(BaseModel):
    """
    Journal header
    """
    #: Journal unique ID
    id: int
    #: operation name
    operation: str
    #: operation description
    description: str
    #: journal creation time
    started_at: datetime
    #: assigned labels
    labels: List[str]
    #: execution end time
    finished_at: Optional[datetime] = None
    #: error message if any
    error: Optional[str] = None
    #: accurate operation duration
    duration: Optional[float] = None

    @classmethod
    def from_database(cls, info: Mapping, labels: List[str]) -> 'Headline':
        return Headline(
            id=info['id'],
            operation=info['operation'],
            description=info['description'],
            started_at=info['started_at'],
            finished_at=info['finished_at'],
            error=info['error'],
            duration=info['duration'],
            labels=labels,
        )


class Journal(Headline):
    """
    Journal entity with header and linked records
    """
    #: journal records
    records: List[Record]


class Journals:
    """
    Journal of logged invokes.

    Should be used as decorator for async methods. Will create, track and record changes automatically.
    In case of exception, the error will be logged and an exception re-raised.

    :Example:

    .. code-block:: python

       from binp import BINP
       from asyncio import sleep

       binp = BINP()

       @binp.journal
       async def invoke():
           '''
           Do something
           '''
           await sleep(3) # emulate some work
           print("done")

    By default, journal will be created with name equal to fully-qualified
    function name and description from doc-string (if exists).

    Name and description could by optionally defined manually.

    .. code-block:: python

       from binp import BINP
       from asyncio import sleep

       binp = BINP()

       @binp.journal(operation='Do Something', description='Emulate some heavy work')
       async def invoke():
           await sleep(3)
           print("done")

    It's possible to add multiple record to journal. Each record contains text message and unlimited number
    of key-value pairs, where value should JSON serializable objects or be subclass of BaseModel (pydantic).


    .. code-block:: python

       from binp import BINP
       from asyncio import sleep

       binp = BINP()

       @binp.journal
       async def invoke():
           await binp.journal.record("begin work", source="http://example.com", by="reddec")
           await sleep(3)
           await binp.journal.record("work done", status="success")

    It's safe to combine journal annotation with any other decorators.

    To get current journal ID use ``current_journal``

    .. code-block:: python

       from binp.journals import current_journal

       binp = BINP()

       @binp.journal
       async def invoke():
           print("Journal ID:", current_journal.get())

    ``current_journal`` can be used only with function decorated by @journal in call chain.
    Otherwise it will return None. The variable is context-depended and coroutine-safe.


    :Events:

    * ``journal_updated`` - when journal created or updated. Emits journal ID
    * ``record_added`` - when record added. Emits journal ID

    **Important!** Never set current journal manually.
    """

    def __init__(self, database: Optional[Database] = None):
        self.__db = ensure(database)
        self.journal_updated: Emitter[int] = Emitter()
        self.record_added: Emitter[int] = Emitter()

    def __call__(self, func=None, *, operation: Optional[str] = None, description: Optional[str] = None):
        """
        Decorator that tracks operation and put it to journal.
        """

        def trace_operation(fn):
            nonlocal operation
            nonlocal description

            if operation is None:
                operation = fn.__qualname__
            if description is None:
                description = "\n".join(line.strip() for line in (fn.__doc__ or '').splitlines()).strip()

            @wraps(fn)
            async def wrapper(*args, **kwargs):

                a = monotonic()
                ex: Optional[Exception] = None
                rec = await self.__begin(operation, description)
                token = current_journal.set(rec)
                try:
                    return await fn(*args, **kwargs)
                except Exception as f_ex:
                    ex = f_ex
                    raise
                finally:
                    current_journal.reset(token)
                    await self.__end(rec, monotonic() - a, ex)

            return wrapper

        if func is None:
            return trace_operation
        return trace_operation(func)

    async def history(self, offset: int = 0, limit: int = 20) -> List[Headline]:
        """
        Get journal headlines in reverse order (newest - first).
        """
        db = await self.__db()
        rows = await db.fetch_all('''
            SELECT * FROM journal ORDER BY id DESC LIMIT :limit OFFSET :offset
        ''', values={
            'offset': offset,
            'limit': limit
        })
        ans = []
        for info in rows:
            labels = await self.__fetch_labels(info['id'])
            ans.append(Headline.from_database(info, labels))
        return ans

    async def search(self, operation: Optional[str] = None,
                     failed: Optional[bool] = None,
                     pending: Optional[bool] = None,
                     labels: Optional[Collection[str]] = None,
                     offset: int = 0,
                     limit: int = 20) -> List[Headline]:
        """
        Search journals. Each condition joined by AND operator. Null conditions will not be applied.
        If no conditions defined, it's equal to plain history() operation.
        Result ordered in reverse order (newest - first).

        :param operation: operation name
        :param failed: with error message
        :param pending: without finished_at attribute
        :param labels: labels names (at least one of list)
        :param offset: how many records to skip
        :param limit: maximum number of records to return
        """
        conditions = []
        args = {
            'offset': offset,
            'limit': limit
        }
        if operation is not None:
            conditions.append('operation = :operation')
            args['operation'] = operation
        if failed is not None:
            if failed:
                conditions.append('error IS NOT NULL')
            else:
                conditions.append('error IS NULL')
        if pending is not None:
            if pending:
                conditions.append('finished_at IS NULL')
            else:
                conditions.append('finished_at IS NOT NULL')
        if labels is not None:
            opts = []
            for i, label in enumerate(labels):
                key = f'label_{i}'
                args[key] = label
                opts.append(":" + key)

            conditions.append(
                f'id IN (SELECT distinct(journal_id) FROM journal_label WHERE label IN ({",".join(opts)}))')

        if len(conditions) == 0:
            return await self.history(offset, limit)

        where = ' AND '.join(conditions)
        query = f'SELECT journal.* FROM journal WHERE {where} ORDER BY id LIMIT :limit OFFSET :offset'
        getLogger(self.__class__.__qualname__).debug('search query: %s', query)
        db = await self.__db()
        rows = await db.fetch_all(query, values=args)

        ans = []
        for info in rows:
            labels = await self.__fetch_labels(info['id'])
            ans.append(Headline.from_database(info, labels))

        return ans

    async def get(self, journal_id: int) -> Optional[Journal]:
        """
        Get single journal by ID
        """
        db = await self.__db()

        info = await db.fetch_one('SELECT * FROM journal WHERE id = :journal_id', values={
            'journal_id': journal_id
        })
        if info is None:
            return None

        headline = await self.headline(journal_id)
        if headline is None:
            return None

        records = await self.__fetch_records(journal_id)

        return Journal(
            records=records,
            **dict(headline),
        )

    async def headline(self, journal_id: int) -> Optional[Headline]:
        """
        Get single journal headline (without records) by ID
        """
        db = await self.__db()

        info = await db.fetch_one('SELECT * FROM journal WHERE id = :journal_id', values={
            'journal_id': journal_id
        })
        if info is None:
            return None
        labels = await self.__fetch_labels(journal_id)
        return Headline.from_database(info, labels)

    async def labels(self, *labels: str):
        """
        Assign labels to journal. Duplicated labels will be ignored. Only under @journal function.
        """
        logger = getLogger(self.__class__.__qualname__)
        journal_id = current_journal.get()
        if journal_id is None:
            logger.warning('function no marked as @journal - label will not be assigned')
            return
        db = await self.__db()
        await db.execute_many('INSERT OR IGNORE INTO journal_label (journal_id, label) VALUES (:journal_id, :label)',
                              values=[
                                  {'journal_id': journal_id, 'label': label} for label in labels
                              ])

    async def record(self, message: str, **events: Union[BaseModel, str, int, float, bool]):
        """
        Add record to journal. Will work only if there is
        @journal function in call chain.

        :param message: short message, describes record
        :param events: key->value of events, where key is event name, and value is basic type or pydantic model.
                       Value will be serialized as JSON
        """
        logger = getLogger(self.__class__.__qualname__)
        journal_id = current_journal.get()
        if journal_id is None:
            logger.warning('function no marked as @journal - event will not be published')
            return

        db = await self.__db()

        async with db.transaction():
            await db.execute('''INSERT INTO record (journal_id, message) VALUES (:journal_id, :message)''', values={
                'journal_id': journal_id,
                'message': message or '',
            })
            record_id = (await db.fetch_one('SELECT last_insert_rowid()'))[0]
            logger.info(message)
            await db.execute_many('''INSERT INTO record_field (record_id, name, value) 
                                   VALUES (:record_id, :name, :value)
                                   ''', values=[{
                'name': name,
                'value': value.json() if isinstance(value, BaseModel) else dumps(value, ensure_ascii=False),
                'record_id': record_id
            } for name, value in events.items()])
        self.record_added.emit(journal_id)

    async def remove_dead(self):
        """
        Remove all records without finish_at timestamp. Should be called only once BEFORE any writes.
        """
        db = await self.__db()
        await db.execute('''
                   DELETE FROM journal
                   WHERE finished_at IS NULL
               ''')

    @property
    def current(self) -> Optional[int]:
        """
        Helper to get current journal ID
        """
        return current_journal.get()

    async def __fetch_labels(self, journal_id: int) -> List[str]:
        db = await self.__db()
        rows = await db.fetch_all('SELECT label FROM journal_label WHERE journal_id = :journal_id', values={
            'journal_id': journal_id
        })
        if rows is None:
            return []
        return [row['label'] for row in rows]

    async def __fetch_records(self, journal_id: int) -> List[Record]:
        db = await self.__db()
        rows = await db.fetch_all('SELECT * FROM record WHERE journal_id = :journal_id ORDER BY id DESC', values={
            'journal_id': journal_id
        })
        if rows is None or len(rows) == 0:
            return []
        result = []
        for row in rows:
            fields = await self.__fetch_fields(row['id'])
            result.append(Record(
                message=row['message'],
                created_at=row['created_at'],
                params=fields
            ))
        return result

    async def __fetch_fields(self, record_id: int) -> Dict[str, Any]:
        db = await self.__db()
        rows = await db.fetch_all('SELECT name, value FROM record_field WHERE record_id = :record_id', values={
            'record_id': record_id
        })
        if rows is None or len(rows) == 0:
            return {}
        return dict((row['name'], loads(row['value'])) for row in rows)

    async def __begin(self, name, description) -> int:
        db = await self.__db()

        async with db.transaction():
            await db.execute('''INSERT INTO journal (operation, description) 
                        VALUES (:operation, :description)
                        ''', values={
                'operation': name,
                'description': description,
            })
            res = await db.fetch_one('SELECT last_insert_rowid()')

        journal_id = res[0]
        self.journal_updated.emit(journal_id)
        return journal_id

    async def __end(self, journal_id: int, delta: float, exc=None):
        db = await self.__db()
        await db.execute('''
        UPDATE journal
        SET finished_at = current_timestamp,
            duration = :duration,
            error = :error
        WHERE id = :id                
                            ''', values={
            'duration': delta,
            'id': journal_id,
            'error': str(exc) if exc is not None else None
        })
        self.journal_updated.emit(journal_id)
