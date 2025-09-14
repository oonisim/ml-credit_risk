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
echo "Creating PostgreSQL online store database ${PG_ONLINE_DB} if not exists..."
echo "--------------------------------------------------------------------------------"
if [[ -z "${PG_ONLINE_PASSWORD:-}" ]]; then
  echo "Need the password for the online store database user ${PG_ONLINE_USER}."
  read -r -s -p "Enter the offline store database user password: " PG_ONLINE_PASSWORD
  echo  # Add newline after password input
  trap 'unset PG_ONLINE_PASSWORD' EXIT
fi


create_postgres_db_and_user \
  "${PG_ONLINE_DB}" \
  "${PG_ONLINE_USER}" \
  "${PG_ONLINE_SCHEMA}" \
  "${PG_ONLINE_HOST}" \
  "${PG_ONLINE_PORT}" \
  "${PG_ONLINE_PASSWORD}" \
  "${PG_ADMIN_USER}"
