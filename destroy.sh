#!/usr/bin/env bash

DIR="$(realpath "$(dirname "${0}")")"
cd "${DIR}" || exit

./deployment/feast/feature_repository/destroy.sh
./deployment/infra/sh/destroy.sh
