#!/bin/bash

DB_NAME="piscineds"
DB_USER="dlu"
DB_HOST="localhost"
DB_PORT="5432"
PGPASSWORD="mysecretpassword"

export PGPASSWORD

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