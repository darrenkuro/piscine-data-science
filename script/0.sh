#!/bin/bash

DB_NAME="piscineds"
DB_USER="dlu"
DB_HOST="localhost"
DB_PORT="5432"
DIR_NAME="customer"
PGPASSWORD="mysecretpassword"

export PGPASSWORD

if [ ! -d "$DIR_NAME" ]; then
    echo "Directory '$DIR_NAME' does not exist."
    exit 1
fi

shopt -s nullglob
for file in "$DIR_NAME"/*.csv; do
    table=$(basename "$file" .csv)
    CMD="
    DROP TABLE IF EXISTS $table;
    CREATE TABLE IF NOT EXISTS $table (
        event_time timestamp NOT NULL,
        event_type text NOT NULL,
        product_id int NOT NULL,
        price money NOT NULL,
        user_id bigint NOT NULL,
        user_session UUID
    );
    "
    psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -c "$CMD"
    psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -c "\copy \"$table\" FROM '$file' WITH (FORMAT csv, HEADER true)"
done

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