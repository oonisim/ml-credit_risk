#!/usr/bin/env bash

DIR="$(realpath "$(dirname "${0}")")"
cd "${DIR}" || exit

./feast/feature_repository/destroy.sh
./local/sh/destroy.sh
