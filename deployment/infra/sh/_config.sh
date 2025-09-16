# Docker
readonly IMAGE_NAME="postgres:15"
readonly CONTAINER_NAME="psql15"

# PostgreSQL
readonly PG_ADMIN_USER='postgres'
readonly PGPASS_FILE="${HOME}/.pgpass"

# FEAST registry database
readonly PG_FEAST_USER="${PG_ADMIN_USER}"
readonly PG_FEAST_DB="feast_registry"
readonly PG_FEAST_HOST="localhost"
readonly PG_FEAST_PORT="5432"

# Offline database
readonly PG_OFFLINE_HOST="localhost"
readonly PG_OFFLINE_PORT="5432"
readonly PG_OFFLINE_USER='dbadm'
readonly PG_OFFLINE_DB="offline_features"
readonly PG_OFFLINE_SCHEMA='credit'

# Online database
readonly PG_ONLINE_HOST="localhost"
readonly PG_ONLINE_PORT="5432"
readonly PG_ONLINE_USER='dbadm'
readonly PG_ONLINE_DB="online_features"
readonly PG_ONLINE_SCHEMA='credit'
