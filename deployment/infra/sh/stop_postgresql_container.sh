#!/usr/bin/env bash
set -e
DIR="$(realpath "$(dirname "${0}")")"
cd "${DIR}" || exit

. _config.sh

echo "--------------------------------------------------------------------------------"
echo "Stopping and removing PostgreSQL container..."
echo "--------------------------------------------------------------------------------"

if docker inspect "${CONTAINER_NAME}" >/dev/null 2>&1; then
    echo "Container ${CONTAINER_NAME} exists. Stopping and removing..."
    docker stop "${CONTAINER_NAME}" 2>/dev/null || true
    docker rm "${CONTAINER_NAME}" 2> /dev/null || true
    echo "Container ${CONTAINER_NAME} removed successfully"
else
    echo "Container ${CONTAINER_NAME} does not exist"
fi