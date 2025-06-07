#!/bin/bash

# Database config variables
DB_NAME="piscineds"
DB_USER="dlu"
DB_HOST="localhost"
DB_PORT="5432"
PGPASSWORD="mysecretpassword"

export PGPASSWORD

# SQL command to remove duplicate
CMD="
    WITH deduplicated AS (
      SELECT *,
            LAG(event_time) OVER (
                PARTITION BY event_type, product_id, user_id
                ORDER BY event_time
            ) AS prev_time
      FROM customers
    )
    DELETE FROM customers
    WHERE ctid IN (
        SELECT ctid
        FROM deduplicated
        WHERE prev_time IS NOT NULL
          AND EXTRACT(EPOCH FROM event_time - prev_time) <= 1
    );"

psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -c "$CMD"