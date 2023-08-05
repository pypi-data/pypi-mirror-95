CREATE TABLE journal_label
(
    journal_id BIGINT NOT NULL REFERENCES journal (id),
    label      TEXT   NOT NULL,
    PRIMARY KEY (journal_id, label)
);

CREATE INDEX journal_label_journal_idx ON journal_label (journal_id);
CREATE INDEX journal_label_label_idx ON journal_label (label);