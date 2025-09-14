#!/usr/bin/env bash
set -e
DIR="$(realpath "$(dirname "${0}")")"
cd "${DIR}" || exit

echo
echo "--------------------------------------------------------------------------------"
echo "Running feast teardown"
echo "--------------------------------------------------------------------------------"
feast teardown || echo "teardown failed."
