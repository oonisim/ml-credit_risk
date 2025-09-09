#!/usr/bin/env bash
set -e
DIR="$(realpath "$(dirname "${0}")")"
cd "${DIR}" || exit

feast apply
feast materialize-incremental "$(date +%Y-%m-%d)"
