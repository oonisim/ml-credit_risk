validate_postgresql_identifier() {
  local v="$1"
  if [[ ! "$v" =~ ^[a-zA-Z_][a-zA-Z0-9_]*$ ]]; then
    echo "Invalid identifier: $v" >&2
    exit 1
  fi
}

check_postgres_ready() {
  local host="${1:? Set PostgreSQL Host}"
  local port="${2:? Set PostgreSQL Port}"

  if ! command -v pg_isready >/dev/null 2>&1; then
    echo "pg_isready not found; proceeding without readiness check"
    return 0
  fi

  if ! pg_isready -h "$host" -p "$port"; then
    echo "Postgres not ready at ${host}:${port}" >&2
    exit 1
  fi
}


# Create a PostgreSQL password entry in ${HOME}/.pgpass
# setup_pgpass_entry "localhost" "5432" "mydatabase" "postgres" "mypassword"
setup_pgpass_entry() {

    echo "setup_pgpass_entry: "
    local host="${1:-localhost}"
    local port="${2:-5432}"
    local database="${3:-*}"
    local user="${4:-postgres}"
    local password="${5:?Provide POSTGRES_PASSWORD}"

    echo "setup_pgpass_entry: password=${password}"


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


create_postgres_db_and_user() {
  local DB_NAME="${1:?Provide DB_NAME}"
  local DB_USER="${2:?Provide DB_USER}"
  local DB_SCHEMA="${3:?Provide DB_SCHEMA}"
  local DB_HOST="${4:-localhost}"
  local DB_PORT="${5:-5432}"
  local DB_PASSWORD="${6:?provide DB_PASSWORD}"
  local ADMIN_USER=${7:?provide ADMIN_USER}

  check_postgres_ready "${DB_HOST}" "${DB_PORT}"
  validate_postgresql_identifier "${DB_SCHEMA}"
  validate_postgresql_identifier "${DB_USER}"

  # Check required arguments
    if [[ -z "$DB_NAME" ]]; then
      echo "Error: DB_NAME (argument 1) is not set" >&2
      exit 1
    fi

    if [[ -z "$DB_USER" ]]; then
      echo "Error: DB_USER (argument 2) is not set" >&2
      exit 1
    fi

    if [[ -z "$DB_SCHEMA" ]]; then
      echo "Error: DB_SCHEMA (argument 3) is not set" >&2
      exit 1
    fi

    if [[ -z "$DB_PASSWORD" ]]; then
      echo "Error: DB_PASSWORD (argument 6) is not set" >&2
      exit 1
    fi

  # Validate identifiers
  for ident in "$DB_NAME" "$DB_USER" "$DB_SCHEMA"; do
    if [[ ! "$ident" =~ ^[a-zA-Z_][a-zA-Z0-9_]*$ ]]; then
      echo "Invalid identifier: $ident" >&2
      return 1
    fi
  done

  # Prompt for password if not set
  if [[ -z "$DB_PASSWORD" ]]; then
    read -r -s -p "Enter password for ${DB_USER}: " DB_PASSWORD
    echo
    trap 'unset DB_PASSWORD' EXIT
  fi

  # Check PostgreSQL readiness
  if command -v pg_isready >/dev/null 2>&1; then
    pg_isready -h "$DB_HOST" -p "$DB_PORT" || {
      echo "Postgres not ready at $DB_HOST:$DB_PORT" >&2
      return 1
    }
  else
    echo "pg_isready not found; skipping readiness check"
  fi

  echo "--------------------------------------------------------------------------------"
  echo "Creating database $DB_NAME if it does not exist..."
  echo "--------------------------------------------------------------------------------"
  if ! psql -h "$DB_HOST" -p "$DB_PORT" -U "$ADMIN_USER" -tAc \
       "SELECT 1 FROM pg_database WHERE datname='$DB_NAME';" | grep -q 1; then
    psql -h "$DB_HOST" -p "$DB_PORT" -U "$ADMIN_USER" -c "CREATE DATABASE $DB_NAME;"
  fi

  echo "Creating user $DB_USER if not exists..."
  if ! psql -h "$DB_HOST" -p "$DB_PORT" -U "$ADMIN_USER" -tAc \
       "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER';" | grep -q 1; then
    psql -h "$DB_HOST" -p "$DB_PORT" -U "$ADMIN_USER" \
         -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
  fi

  echo "Creating schema $DB_SCHEMA and granting privileges..."
  psql -h "$DB_HOST" -p "$DB_PORT" -U "$ADMIN_USER" -d "$DB_NAME" -c "
CREATE SCHEMA IF NOT EXISTS $DB_SCHEMA;
GRANT CONNECT ON DATABASE $DB_NAME TO $DB_USER;
GRANT USAGE, CREATE ON SCHEMA $DB_SCHEMA TO $DB_USER;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA $DB_SCHEMA TO $DB_USER;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA $DB_SCHEMA TO $DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA $DB_SCHEMA
    GRANT ALL ON TABLES TO $DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA $DB_SCHEMA
    GRANT ALL ON SEQUENCES TO $DB_USER;
ALTER USER $DB_USER SET search_path TO $DB_SCHEMA, public;
"

  echo "Setting up .pgpass..."
  setup_pgpass_entry "$DB_HOST" "$DB_PORT" "$DB_NAME" "$DB_USER" "$DB_PASSWORD"

  echo "Setup completed! Connect with:"
  echo "psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME"
}
