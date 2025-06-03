#!/bin/bash

DB_NAME="piscineds"
DB_USER="dlu"
DB_HOST="localhost"
DB_PORT="5432"
PGPASSWORD="mysecretpassword"
TABLE=items
CSV_PATH="./item/item.csv"

export PGPASSWORD

if [ ! -f "$CSV_PATH" ]; then
  echo "File not found: $CSV_PATH"
  exit 1
fi

CMD="
DROP TABLE IF EXISTS $TABLE;
CREATE TABLE IF NOT EXISTS $TABLE (
    product_id int NOT NULL,
    category_id bigint,
    category_code text,
    brand text
);
"

psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -c "$CMD"
psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -c "\copy \"$TABLE\" FROM '$CSV_PATH' WITH (FORMAT csv, HEADER true)"