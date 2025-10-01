#!/usr/bin/env bash
set -eo pipefail
DIR="$(realpath "$(dirname "${0}")")"
cd "${DIR}" || exit 1


if [[ -z "${POSTGRES_PASSWORD}" ]]; then
  echo
  echo "--------------------------------------------------------------------------------"
  echo "Setting up administrative prerequisite..."
  echo "--------------------------------------------------------------------------------"
  echo "Provide a new password for the Docker PostgreSQL administration."
  echo "Alternatively, set the environment variable POSTGRES_PASSWORD as" \
       "'export POSTGRES_PASSWORD=... before running this script."
  read -r -s -p "> " POSTGRES_PASSWORD
  echo
  if [[ -z "${POSTGRES_PASSWORD}" ]]; then
    echo "Error: POSTGRES_PASSWORD cannot be empty" >&2
    exit 1
  fi
  export "POSTGRES_PASSWORD=${POSTGRES_PASSWORD}"
  trap 'unset POSTGRES_PASSWORD' EXIT
fi

printf "\n\n"
chmod u+x ./deployment/infra/sh/deploy.sh
./deployment/infra/sh/deploy.sh

chmod u+x ./deployment/feast/feature_repository/deploy.sh
./deployment/feast/feature_repository/deploy.sh

echo
echo "Create and activate a Python virtual environment and " \
     "run 'pip install -r requirements.txt' to install Python dependencies."
echo "Then run 'python -m notebook' to start the Jupyter Notebook."