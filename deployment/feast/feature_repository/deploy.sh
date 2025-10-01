#!/usr/bin/env bash
set -eo pipefail
DIR="$(realpath "$(dirname "${0}")")"
cd "${DIR}" || exit 1

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
if [[ -z "${POSTGRES_PASSWORD:-}" ]]; then
    echo "Error: POSTGRES_PASSWORD not set" >&2
    exit 1
fi

readonly PATH_TO_CONFIG="../../infra/sh/_config.sh"
check_file_exists "${PATH_TO_CONFIG}"

set -a  # Auto-export variables
source "${PATH_TO_CONFIG}"
set +a

if [[ -f "feature_store.yaml" && ! -f "feature_store.yaml.bak" ]]; then
    echo "Backing up existing feature_store.yaml..."
    mv feature_store.yaml feature_store.yaml.bak
    chmod go-rwx feature_store.yaml.bak
fi
envsubst < feature_store.yaml.template > feature_store.yaml
