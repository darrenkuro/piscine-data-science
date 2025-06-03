#!/bin/bash

DB_NAME="piscineds"
DB_USER="dlu"
DB_HOST="localhost"
DB_PORT="5432"
PGPASSWORD="mysecretpassword"

export PGPASSWORD

CMD="
CREATE TEMPORARY TABLE temp_customers AS
WITH deduplicated AS (
  SELECT *,
    LAG(event_time) OVER (
        PARTITION BY event_type, product_id
        ORDER BY event_time
    ) AS prev_time
  FROM (
    SELECT DISTINCT * FROM customers
  ) AS distinct_rows
)
SELECT event_time, event_type, product_id, price, user_id, user_session
FROM deduplicated
WHERE prev_time IS NULL
   OR EXTRACT(EPOCH FROM event_time - prev_time) > 1;

TRUNCATE customers;
INSERT INTO customers SELECT * FROM temp_customers;
"

psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -c "$CMD"