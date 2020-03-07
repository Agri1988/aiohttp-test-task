#!/usr/bin/env bash

set -e
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER test_user WITH PASSWORD 'testpswd';
    CREATE DATABASE test_task;
    GRANT ALL PRIVILEGES ON DATABASE test_task TO test_user;
    ALTER ROLE test_user SET client_encoding TO 'utf8';
    ALTER ROLE test_user SET default_transaction_isolation TO 'read committed';
    ALTER ROLE test_user SET timezone TO 'UTC';
EOSQL