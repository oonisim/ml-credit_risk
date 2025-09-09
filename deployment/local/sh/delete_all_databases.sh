#!/usr/bin/env bash
set -e
DIR="$(realpath "$(dirname "${0}")")"
cd "${DIR}" || exit

PG_HOST="localhost"
PG_PORT="5432"
PG_USER="postgres"

echo "--------------------------------------------------------------------------------"
echo "Delete All User Databases in PostgreSQL..."
echo "--------------------------------------------------------------------------------"

echo "⚠️  WARNING: This will drop ALL user databases!"
echo "System databases (postgres, template0, template1) will be preserved."
read -r -p "Are you sure? (yes/no): " confirm

if [ "$confirm" = "yes" ]; then
    # Get list of user databases (exclude system databases)
    USER_DBS=$(psql -h $PG_HOST -p $PG_PORT -U $PG_USER \
       -tAc "SELECT datname FROM pg_database
             WHERE
               datistemplate = false
               AND datname NOT IN ('postgres');"
    )

    for db in $USER_DBS; do
        echo "Dropping database: $db"
        psql -h $PG_HOST -p $PG_PORT -U $PG_USER \
             -c "DROP DATABASE IF EXISTS \"$db\";"
    done

    echo "✅ All user databases dropped"
else
    echo "❌ Operation cancelled"
fi