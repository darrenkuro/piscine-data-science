#!/bin/bash

DB_NAME="piscineds"
DB_USER="dlu"
DB_HOST="localhost"
DB_PORT="5432"
PGPASSWORD="mysecretpassword"
TABLE="data_2022_dec"

export PGPASSWORD

CMD="
DROP TABLE IF EXISTS $TABLE;
CREATE TABLE IF NOT EXISTS $TABLE (
    event_time TIMESTAMP NOT NULL,
    event_type TEXT NOT NULL,
    product_id INT NOT NULL,
    price MONEY NOT NULL,
    user_id BIGINT NOT NULL,
    user_session UUID
);
"

psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -c "$CMD"