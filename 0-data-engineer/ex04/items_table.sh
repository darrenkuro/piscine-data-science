#!/bin/bash

DB_NAME="piscineds"
DB_USER="dlu"
DB_HOST="localhost"
DB_PORT="5432"

export PGPASSWORD="mysecretpassword"

psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -c "
CREATE TABLE IF NOT EXISTS items (
    product_id int NOT NULL,
    category_id bigint NOT NULL,
    category_code text,
    brand text
);
"