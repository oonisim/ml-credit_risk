#!/usr/bin/env bash
set -e

DIR="$(realpath "$(dirname "${0}")")"
cd "${DIR}" || exit

./local/sh/deploy.sh
#./feast/feature_repository/deploy.sh
