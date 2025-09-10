#!/usr/bin/env bash
set -e
DIR="$(realpath "$(dirname "${0}")")"
cd "${DIR}" || exit

. _config.sh
. _utility.sh

echo "--------------------------------------------------------------------------------"
echo "Creating PostgreSQL offline store database ${PG_OFFLINE_DB} if not exists..."
echo "--------------------------------------------------------------------------------"

read -r -s -p "Enter FEAST offline store database password: " PG_OFFLINE_PASSWORD
echo  # Add newline after password input

psql -h "${PG_OFFLINE_HOST}" -p "${PG_OFFLINE_PORT}" -U "${PG_ADMIN_USER}" -lqt \
  | cut -d \| -f 1 \
  | grep -qw "${PG_OFFLINE_DB}" || {
    psql -h "${PG_OFFLINE_HOST}" \
         -p "${PG_OFFLINE_PORT}" \
         -U "${PG_ADMIN_USER}" \
         -c "CREATE DATABASE ${PG_OFFLINE_DB};"
}

echo "Creating te user ${PG_OFFLINE_USER} for offline store database..."
# Create user if not exists
psql -h "${PG_OFFLINE_HOST}" \
     -p "${PG_OFFLINE_PORT}" \
     -U "${PG_ADMIN_USER}" \
     -tAc "SELECT 1 FROM pg_roles WHERE rolname='${PG_OFFLINE_USER}'" \
  | grep -q 1 || {
    psql -h "${PG_OFFLINE_HOST}" \
         -p "${PG_OFFLINE_PORT}" \
         -U "${PG_ADMIN_USER}" \
         -c "CREATE USER ${PG_OFFLINE_USER} WITH PASSWORD '${PG_OFFLINE_PASSWORD:?PG_OFFLINE_PASSWORD not set}';"
}

echo "Creating te schema ${PG_OFFLINE_SCHEMA} and grant permissions to ${PG_OFFLINE_USER}..."
psql -h "${PG_OFFLINE_HOST}" \
     -p "${PG_OFFLINE_PORT}" \
     -U "${PG_ADMIN_USER}" \
     -d "${PG_OFFLINE_DB}" \
     -c "
CREATE SCHEMA IF NOT EXISTS ${PG_OFFLINE_SCHEMA};
GRANT CONNECT ON DATABASE ${PG_OFFLINE_DB} TO ${PG_OFFLINE_USER};
GRANT USAGE, CREATE ON SCHEMA ${PG_OFFLINE_SCHEMA} TO ${PG_OFFLINE_USER};
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA ${PG_OFFLINE_SCHEMA} TO ${PG_OFFLINE_USER};
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA ${PG_OFFLINE_SCHEMA} TO ${PG_OFFLINE_USER};
ALTER DEFAULT PRIVILEGES IN SCHEMA ${PG_OFFLINE_SCHEMA}
    GRANT ALL ON TABLES TO ${PG_OFFLINE_USER};
ALTER DEFAULT PRIVILEGES IN SCHEMA ${PG_OFFLINE_SCHEMA}
    GRANT ALL ON SEQUENCES TO ${PG_OFFLINE_USER};
ALTER USER ${PG_OFFLINE_USER} SET search_path TO ${PG_OFFLINE_SCHEMA}, public;
"

echo "Setting up PostgreSQL password file (.pgpass)..."
setup_pgpass_entry \
  "${PG_OFFLINE_HOST}" \
  "${PG_OFFLINE_PORT}" \
  "${PG_OFFLINE_DB}" \
  "${PG_OFFLINE_USER}" \
  "${PG_OFFLINE_PASSWORD}"

echo "Setup completed! Connect with:"
echo "psql -h ${PG_OFFLINE_HOST} -p ${PG_OFFLINE_PORT} -U ${PG_OFFLINE_USER} -d ${PG_OFFLINE_DB}"