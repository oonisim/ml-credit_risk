#!/usr/bin/env bash
set -e
DIR="$(realpath "$(dirname "${0}")")"
cd "${DIR}" || exit

. _config.sh
. _utility.sh

echo "--------------------------------------------------------------------------------"
echo "Creating FEAST Registry database in PostgreSQL if it doesn't exist..."
echo "--------------------------------------------------------------------------------"

if psql -h "${PG_FEAST_HOST}" \
        -p "${PG_FEAST_PORT}" \
        -U "${PG_ADMIN_USER}" \
        -lqt | cut -d \| -f 1 | grep -qw "${PG_FEAST_DB}"; then
    echo "Database $PG_FEAST_DB already exists"
else
    echo "Creating database ${PG_FEAST_DB}..."
    PG_FEAST_PASSWORD="${POSTGRES_PASSWORD:?POSTGRES_PASSWORD is not set}}"

    psql -h "${PG_FEAST_HOST}" \
         -p "${PG_FEAST_PORT}" \
         -U "${PG_ADMIN_USER}" \
         -c "CREATE DATABASE ${PG_FEAST_DB} WITH ENCODING = 'UTF8';"

    echo "Setting up PostgreSQL password file (.pgpass)..."
    setup_pgpass_entry \
      "${PG_FEAST_HOST}" \
      "${PG_FEAST_PORT}" \
      "${PG_FEAST_DB}" \
      "${PG_FEAST_USER}" \
      "${PG_FEAST_PASSWORD}"

    echo "Database ${PG_FEAST_DB} created successfully."
fi