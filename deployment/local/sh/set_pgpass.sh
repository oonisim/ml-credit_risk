#!/bin/bash
set -e

setup_pgpass_entry() {
    local host="${1:-localhost}"
    local port="${2:-5432}"
    local database="${3:-*}"
    local user="${4:-postgres}"
    local password="${5:-${POSTGRES_PASSWORD:?POSTGRES_PASSWORD is not set}}"

    local pgpass_file="${HOME}/.pgpass"
    local pgpass_entry="${host}:${port}:${database}:${user}:${password}"

    echo "Setting up PostgreSQL password entry for ${user}@${host}:${port}..."

    # Check if file exists and contains the entry
    if [ ! -f "$pgpass_file" ] || ! grep -Fq "$pgpass_entry" "$pgpass_file" 2>/dev/null; then
        echo "Adding PostgreSQL password entry..."
        echo "$pgpass_entry" >> "$pgpass_file"
        chmod 600 "$pgpass_file"
        echo "✅ Entry added to $pgpass_file"
    else
        echo "✅ Entry already exists in $pgpass_file"
    fi
}

# Usage examples
DIR="$(realpath "$(dirname "${0}")")"
cd "${DIR}" || exit

echo "--------------------------------------------------------------------------------"
echo "Setting up PostgreSQL password file (.pgpass)..."
echo "--------------------------------------------------------------------------------"

# Use with default parameters
setup_pgpass_entry

# Or with custom parameters
# setup_pgpass_entry "localhost" "5432" "mydatabase" "postgres" "mypassword"