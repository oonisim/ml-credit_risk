#!/usr/bin/env bash
set -e
. ./config.sh

echo "--------------------------------------------------------------------------------"
echo "Creating FEAST Registry database in PostgreSQL if it doesn't exist..."
echo "--------------------------------------------------------------------------------"

if psql -h "${PG_FEAST_HOST}" \
        -p "${PG_FEAST_PORT}" \
        -U "${PG_ADMIN_USER}" \
        -lqt | cut -d \| -f 1 | grep -qw "${PG_FEAST_DB}"; then
    echo "Database $PG_FEAST_DB already exists"
else
    echo "Creating database $PG_FEAST_DB"
    psql -h "${PG_FEAST_HOST}" \
         -p "${PG_FEAST_PORT}" \
         -U "${PG_ADMIN_USER}" \
         -c "CREATE DATABASE ${PG_FEAST_DB} WITH ENCODING = 'UTF8';"
    echo "Database $PG_FEAST_DB created successfully"
fi