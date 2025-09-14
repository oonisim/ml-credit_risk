#!/usr/bin/env bash
set -eo pipefail
DIR="$(realpath "$(dirname "${0}")")"
cd "${DIR}" || exit

chmod u+x *.sh

. _prerequisite.sh
./start_postgresql_container.sh
./create_registry_database.sh
./create_offline_store_database.sh
