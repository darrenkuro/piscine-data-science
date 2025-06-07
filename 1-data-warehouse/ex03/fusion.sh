#!/bin/bash

# Database config variables
DB_NAME="piscineds"
DB_USER="dlu"
DB_HOST="localhost"
DB_PORT="5432"
PGPASSWORD="mysecretpassword"

export PGPASSWORD

# SQL command to combine customers and items
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