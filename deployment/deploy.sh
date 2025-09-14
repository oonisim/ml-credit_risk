#!/usr/bin/env bash
set -e

DIR="$(realpath "$(dirname "${0}")")"
cd "${DIR}" || exit

./infra/sh/deploy.sh
# feast apply is after offline store is loaded.
#./feast/feature_repository/deploy.sh
