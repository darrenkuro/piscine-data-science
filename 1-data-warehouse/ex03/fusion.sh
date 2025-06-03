#!/bin/bash

DB_NAME="piscineds"
DB_USER="dlu"
DB_HOST="localhost"
DB_PORT="5432"
PGPASSWORD="mysecretpassword"

export PGPASSWORD

CMD="
ALTER TABLE customers ADD COLUMN IF NOT EXISTS category_id BIGINT;
ALTER TABLE customers ADD COLUMN IF NOT EXISTS category_code TEXT;
ALTER TABLE customers ADD COLUMN IF NOT EXISTS brand TEXT;

UPDATE customers c
SET
    category_id = i.category_id,
    category_code = i.category_code,
    brand = i.brand
FROM items i
WHERE c.product_id = i.product_id;
"

psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -c "$CMD"