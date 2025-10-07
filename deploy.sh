#!/usr/bin/env bash
set -eo pipefail
DIR="$(realpath "$(dirname "${0}")")"
cd "${DIR}" || exit 1


ensure_macos_bash5() {
    # Skip if we've already upgraded bash
    echo "DEBUG: Function called with BASH_VERSION='$BASH_VERSION'"
    echo "DEBUG: Major version extracted='${BASH_VERSION%%.*}'"

    if [ "$BASH_UPGRADED" = "1" ]; then
        return 0
    fi

    local required_major=5
    local newbash
    echo "--------------------------------------------------------------------------------"
    echo "Verifying bash >= ${required_major} on macOS..."
    echo "--------------------------------------------------------------------------------"

    # Check if current Bash version is sufficient
    if [ -n "$BASH_VERSION" ] && [ "${BASH_VERSION%%.*}" -ge "$required_major" ]; then
        echo "Bash version is ${BASH_VERSION}."
        return 0  # Current bash is good enough
    fi

    # Get Homebrew bash path
    if ! newbash="$(brew --prefix 2>/dev/null)/bin/bash"; then
        echo "ERROR: Unable to determine Homebrew prefix" >&2
        exit 1
    fi

    # Install if not present
    if [ ! -x "$newbash" ]; then
        echo "ERROR: Bash >= ${required_major} required. Installing with: brew install bash" >&2
        if command -v brew >/dev/null 2>&1; then
            if ! brew install bash; then
                echo "ERROR: Failed to install bash via Homebrew" >&2
                exit 1
            fi
        else
            echo "ERROR: Homebrew not found. Please install Homebrew first." >&2
            exit 1
        fi
    fi

    # Execute with newer bash and set flag
    export BASH_UPGRADED=1
    exec "$newbash" "$0" "$@"
}

# MacOS default bash 3.2.x works for this script.
# if [[ "$OSTYPE" == "darwin"* ]]; then
#     ensure_macos_bash5 "$@"
#fi


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