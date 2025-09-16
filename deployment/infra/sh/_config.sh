# Docker
IMAGE_NAME="postgres:15"
CONTAINER_NAME="psql15"

# PostgreSQL
PG_ADMIN_USER='postgres'
PGPASS_FILE="${HOME}/.pgpass"

# FEAST registry database
PG_FEAST_USER="${PG_ADMIN_USER}"
PG_FEAST_DB="feast_registry"
PG_FEAST_HOST="localhost"
PG_FEAST_PORT="5432"

# Offline database
PG_OFFLINE_HOST="localhost"
PG_OFFLINE_PORT="5432"
PG_OFFLINE_USER='dbadm'
PG_OFFLINE_DB="offline_features"
PG_OFFLINE_SCHEMA='credit'

# Online database
PG_ONLINE_HOST="localhost"
PG_ONLINE_PORT="5432"
PG_ONLINE_USER='dbadm'
PG_ONLINE_DB="online_features"
PG_ONLINE_SCHEMA='credit'
