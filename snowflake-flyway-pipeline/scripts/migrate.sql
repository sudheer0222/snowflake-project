CREATE TABLE example_table (
    id INT AUTOINCREMENT PRIMARY KEY,
    name STRING NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO example_table (name) VALUES ('Sample Data 1'), ('Sample Data 2');

ALTER TABLE example_table ADD COLUMN description STRING;