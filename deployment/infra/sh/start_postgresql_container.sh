#!/usr/bin/env bash
set -e
DIR="$(realpath "$(dirname "${0}")")"
cd "${DIR}" || exit

. _config.sh

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
# Start PostgreSQL Container
#--------------------------------------------------------------------------------
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "Container ${CONTAINER_NAME} exists. Removing..."
    docker rm -f "${CONTAINER_NAME}"
else
    echo "Container psql15 does not exist."
fi
echo "starting postgres docker container..."
docker run --name psql15 \
  -e POSTGRES_PASSWORD="${POSTGRES_PASSWORD:?Set POSTGRES_PASSWORD}" \
  -p 5432:5432 \
  -d postgres:15

#--------------------------------------------------------------------------------
# Start PostgreSQL Container
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
        echo "✅ PostgreSQL is ready!"
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
