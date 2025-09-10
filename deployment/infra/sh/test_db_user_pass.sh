#!/bin/bash
# test_password.sh

PG_HOST="localhost"
PG_PORT="5432"
PG_USER="dbadm"
PG_DATABASE="postgres"

test_password() {
    local test_password="$1"

    if PGPASSWORD="$test_password" psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -c "SELECT 1;" >/dev/null 2>&1; then
        echo "✅ Password is correct"
        return 0
    else
        echo "❌ Password is incorrect"
        return 1
    fi
}

# Usage
read -r -s -p "Enter password to test: " TEST_PASSWORD
echo
test_password "$TEST_PASSWORD"