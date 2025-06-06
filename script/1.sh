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

tables=$(psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -Atc "
SELECT tablename FROM pg_tables
WHERE tablename ~ '^data_202[0-9]_.{3}$';")

if [ -z "$tables" ]; then
    echo "No table with matching name found."
    exit 1
fi

unionsql=""
for table in $tables; do
    if [ -z "$unionsql" ]; then
        unionsql="SELECT * FROM \"$table\""
    else
        unionsql="$unionsql UNION ALL SELECT * FROM \"$table\""
    fi
done

CMD="
DROP TABLE IF EXISTS customers;
CREATE TABLE customers AS $unionsql;
"

psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -c "$CMD"

CMD="
CREATE TEMPORARY TABLE temp_customers AS
WITH deduplicated AS (
  SELECT *,
    LAG(event_time) OVER (
        PARTITION BY event_type, product_id, user_id
        ORDER BY event_time
    ) AS prev_time
  FROM customers
)
SELECT event_time, event_type, product_id, price, user_id, user_session
FROM deduplicated
WHERE prev_time IS NULL
   OR EXTRACT(EPOCH FROM event_time - prev_time) > 1;

TRUNCATE customers;
INSERT INTO customers SELECT * FROM temp_customers;
"

psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -c "$CMD"

CMD="
ALTER TABLE customers ADD COLUMN IF NOT EXISTS category_id BIGINT;
ALTER TABLE customers ADD COLUMN IF NOT EXISTS category_code TEXT;
ALTER TABLE customers ADD COLUMN IF NOT EXISTS brand TEXT;

WITH merged_items AS (
  SELECT
    product_id,
    MAX(category_id) AS category_id,
    MAX(category_code) AS category_code,
    MAX(brand) AS brand
  FROM items
  GROUP BY product_id
)

UPDATE customers c
SET
    category_id = mi.category_id,
    category_code = mi.category_code,
    brand = mi.brand
FROM merged_items mi
WHERE c.product_id = mi.product_id;
"

psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -c "$CMD"