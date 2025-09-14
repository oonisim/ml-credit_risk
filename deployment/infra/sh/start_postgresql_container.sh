#!/usr/bin/env bash
set -e
DIR="$(realpath "$(dirname "${0}")")"
cd "${DIR}" || exit

. _config.sh
. _utility.sh

echo
echo "--------------------------------------------------------------------------------"
echo "Setting up PostgreSQL..."
echo "--------------------------------------------------------------------------------"
#--------------------------------------------------------------------------------
# Get PostgreSQL Image
#--------------------------------------------------------------------------------
if docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "Image ${IMAGE_NAME} already exists"
else
    echo "Downloading ${IMAGE_NAME}..."
    docker pull "${IMAGE_NAME}"
fi


#--------------------------------------------------------------------------------
# Setup postgres user password
#--------------------------------------------------------------------------------
if [[ -z "${POSTGRES_PASSWORD:-}" ]]; then
  read -r -s -p "Enter PostgreSQL password: " POSTGRES_PASSWORD
  echo
  if [[ -z "$POSTGRES_PASSWORD" ]]; then
    echo "Error: POSTGRES_PASSWORD cannot be empty" >&2
    exit 1
  fi
  # Unset when the shell exits
  trap 'unset POSTGRES_PASSWORD' EXIT

  echo "Setting up PostgreSQL password file (.pgpass) for user ${PG_ADMIN_USER} if not set..."
  setup_pgpass_entry \
    "localhost" \
    "5432" \
    "*" \
    "${PG_ADMIN_USER}" \
    "${POSTGRES_PASSWORD:?POSTGRES_PASSWORD not set}"
fi


#--------------------------------------------------------------------------------
# Start PostgreSQL Container
#--------------------------------------------------------------------------------
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "Container ${CONTAINER_NAME} exists. Removing..."
    docker rm -f "${CONTAINER_NAME}"
else
    echo "Container psql15 does not exist."
fi

echo "Starting PostgreSQL docker container..."
CONTAINER_ID=$(docker run --name "${CONTAINER_NAME}" \
  -e POSTGRES_PASSWORD="${POSTGRES_PASSWORD:?Set POSTGRES_PASSWORD}" \
  -p "${PG_FEAST_PORT}:${PG_FEAST_PORT}" \
  -d "${IMAGE_NAME}" 2>&1) || {
    echo "Failed to start container: $CONTAINER_ID" >&2
    exit 1
}
echo "PostgreSQL container started with Container ID: ${CONTAINER_ID}."
echo "Check logs with: docker logs ${CONTAINER_ID}"


#--------------------------------------------------------------------------------
# Verify PostgrSQL Container
#--------------------------------------------------------------------------------
echo "Checking if PostgreSQL container is running and ready..."
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "Container $CONTAINER_NAME is not running"
    echo "Container status:"
    docker ps -a --filter "name=$CONTAINER_NAME"
    exit 1
fi

echo "Checking PostgreSQL readiness..."
for i in {1..30}; do
    if docker exec "$CONTAINER_NAME" pg_isready -U postgres >/dev/null 2>&1; then
        echo "PostgreSQL is ready!"
        break
    else
        echo "⏳ Waiting for PostgreSQL... ($i/30)"
        sleep 1
    fi
done

if docker exec "$CONTAINER_NAME" pg_isready -U postgres >/dev/null 2>&1; then
    echo "✅ PostgreSQL is fully operational"
    docker exec "$CONTAINER_NAME" psql -U postgres -c "SELECT version();" | head -3
else
    echo "❌ PostgreSQL failed to start properly"
    echo "Container logs:"
    docker logs --tail 20 "$CONTAINER_NAME"
    exit 1
fi
