#!/usr/bin/env bash
set -eu
DIR="$(realpath "$(dirname "${0}")")"
cd "${DIR}" || exit

#feast apply
#feast materialize-incremental "$(date +%Y-%m-%d)"

check_file_exists() {
    local file="$1"
    if [[ ! -f "$file" ]]; then
        echo "Error: $file does not exist." >&2
        return 1
    fi
}

echo
echo "Generating feature_store.yaml from the variables..."
: "${POSTGRES_PASSWORD:?POSTGRES_PASSWORD not set}"
readonly PATH_TO_CONFIG="../../infra/sh/_config.sh"
check_file_exists "${PATH_TO_CONFIG}"

set -a  # Auto-export variables
source "${PATH_TO_CONFIG}"
set +a

mv -f feature_store.yaml feature_store.yaml.bak
envsubst < feature_store.yaml.template > feature_store.yaml
