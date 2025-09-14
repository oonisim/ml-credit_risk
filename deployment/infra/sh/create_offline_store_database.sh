#!/usr/bin/env bash
#--------------------------------------------------------------------------------
# FEAST Online Store Database Creation Script.
# NOTE: The script must be idempotent.
#--------------------------------------------------------------------------------
set -euo pipefail
IFS=$'\n\t'

DIR="$(realpath "$(dirname "${0}")")"
cd "${DIR}" || exit

. _config.sh
. _utility.sh

echo
echo "--------------------------------------------------------------------------------"
echo "Creating PostgreSQL offline store database ${PG_OFFLINE_DB} if not exists..."
echo "--------------------------------------------------------------------------------"
if [[ -z "${PG_OFFLINE_PASSWORD:-}" ]]; then
  echo "Need the password for the offline store database user ${PG_OFFLINE_USER}."
  read -r -s -p "Enter the offline store database user password: " PG_OFFLINE_PASSWORD
  echo  # Add newline after password input
  trap 'unset PG_OFFLINE_PASSWORD' EXIT
fi


create_postgres_db_and_user \
  "${PG_OFFLINE_DB}" \
  "${PG_OFFLINE_USER}" \
  "${PG_OFFLINE_SCHEMA}" \
  "${PG_OFFLINE_HOST}" \
  "${PG_OFFLINE_PORT}" \
  "${PG_OFFLINE_PASSWORD}" \
  "${PG_ADMIN_USER}"
