#!/bin/bash
set -e
DIR="$(realpath "$(dirname "${0}")")"
cd "${DIR}" || exit

echo "--------------------------------------------------------------------------------"
echo "Setting up PostgreSQL password file (.pgpass)..."
echo "--------------------------------------------------------------------------------"

PGPASS_FILE="${HOME}/.pgpass"
HOST="localhost"
PORT="5432"
DATABASE="*"
USER="postgres"
PGPASS_ENTRY="${HOST}:${PORT}:${DATABASE}:${USER}:${POSTGRES_PASSWORD:?POSTGRES_PASSWORD is not set}"

# Check if file exists and contains the entry
if [ ! -f "$PGPASS_FILE" ] || ! grep -Fq "$PGPASS_ENTRY" "$PGPASS_FILE" 2>/dev/null; then
    echo "Adding PostgreSQL password entry..."
    echo "$PGPASS_ENTRY" >> "$PGPASS_FILE"
    chmod 600 "$PGPASS_FILE"
    echo "✅ Entry added to $PGPASS_FILE"
else
    echo "✅ Entry already exists in $PGPASS_FILE"
fi


