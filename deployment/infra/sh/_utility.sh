# Create a PostgreSQL password entry in ${HOME}/.pgpass
# setup_pgpass_entry "localhost" "5432" "mydatabase" "postgres" "mypassword"
setup_pgpass_entry() {
    local host="${1:-localhost}"
    local port="${2:-5432}"
    local database="${3:-*}"
    local user="${4:-postgres}"
    local password="${5:-${POSTGRES_PASSWORD:?POSTGRES_PASSWORD is not set}}"

    echo "host:${host} port:${port} database:${database} user:${user}"

    local pgpass_file="${HOME}/.pgpass"
    local pgpass_entry="${host}:${port}:${database}:${user}:${password}"

    # Check if file exists and contains the entry
    if [ ! -f "$pgpass_file" ] || ! grep -Fq "${pgpass_entry}" "${pgpass_file}" 2>/dev/null; then
        echo "Adding PostgreSQL password entry..."
        echo "${pgpass_entry}" >> "${pgpass_file}"
        chmod 600 "${pgpass_file}"
        echo "✅ Entry added to ${pgpass_file}"
    else
        echo "✅ Entry already exists in ${pgpass_file}"
    fi
}

