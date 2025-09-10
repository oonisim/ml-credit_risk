#!/usr/bin/env bash
set -e
DIR="$(realpath "$(dirname "${0}")")"
cd "${DIR}" || exit

chmod u+x *.sh

./delete_all_databases.sh
./stop_postgresql_container.sh

