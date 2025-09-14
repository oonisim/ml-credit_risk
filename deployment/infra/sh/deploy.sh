#!/usr/bin/env bash
#--------------------------------------------------------------------------------
# FEAST Tutorial Infrastructure Deployment Script
#--------------------------------------------------------------------------------
set -eo pipefail
DIR="$(realpath "$(dirname "${0}")")"
cd "${DIR}" || exit

chmod u+x ./start_postgresql_container.sh
chmod u+x ./create_registry_database.sh
chmod u+x ./create_offline_store_database.sh
# Cannot use PostgreSQL as online store
# https://github.com/feast-dev/feast/issues/5613
#chmod u+x ./create_online_store_database.sh

. _prerequisite.sh
./start_postgresql_container.sh
./create_registry_database.sh
./create_offline_store_database.sh
# Cannot use PostgreSQL as online store
# https://github.com/feast-dev/feast/issues/5613
#./create_online_store_database.sh
