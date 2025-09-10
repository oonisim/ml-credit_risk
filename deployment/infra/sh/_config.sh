# Docker
IMAGE_NAME="postgres:15"
CONTAINER_NAME="psql15"

PG_ADMIN_USER='postgres'

# FEAST registry database
PG_FEAST_DB="feast_registry"
PG_FEAST_HOST="localhost"
PG_FEAST_PORT="5432"

# Offline database
PG_OFFLINE_HOST="localhost"
PG_OFFLINE_PORT="5432"
PG_OFFLINE_USER='dbadm'
PG_OFFLINE_DB="offline_features"
PG_OFFLINE_SCHEMA='credit'

PGPASS_FILE="${HOME}/.pgpass"