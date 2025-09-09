#!/usr/bin/env bash
set -e
DIR="$(realpath "$(dirname "${0}")")"
cd "${DIR}" || exit

chmod u+x *.sh

./start_postgresql_container.sh
./set_pgpass.sh
./create_offline_store_database.sh
./create_registry_database.sh
