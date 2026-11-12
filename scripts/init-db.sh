#!/bin/bash
set -e

echo ">>> A inicializar o Data Warehouse..."

# Cria utilizador e base de dados do DW (se ainda não existirem)
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'dw_user') THEN
            CREATE USER dw_user WITH PASSWORD 'dw_pass';
        END IF;
    END
    \$\$;

    SELECT 'CREATE DATABASE vendas_dw OWNER dw_user'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'vendas_dw')\gexec

    GRANT ALL PRIVILEGES ON DATABASE vendas_dw TO dw_user;
EOSQL

# Cria os schemas dentro de vendas_dw
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "vendas_dw" <<-EOSQL
    CREATE SCHEMA IF NOT EXISTS raw AUTHORIZATION dw_user;
    CREATE SCHEMA IF NOT EXISTS staging AUTHORIZATION dw_user;
    CREATE SCHEMA IF NOT EXISTS intermediate AUTHORIZATION dw_user;
    CREATE SCHEMA IF NOT EXISTS marts AUTHORIZATION dw_user;

    GRANT ALL ON SCHEMA raw TO dw_user;
    GRANT ALL ON SCHEMA staging TO dw_user;
    GRANT ALL ON SCHEMA intermediate TO dw_user;
    GRANT ALL ON SCHEMA marts TO dw_user;
    GRANT ALL ON SCHEMA public TO dw_user;

    ALTER DEFAULT PRIVILEGES IN SCHEMA raw GRANT ALL ON TABLES TO dw_user;
    ALTER DEFAULT PRIVILEGES IN SCHEMA staging GRANT ALL ON TABLES TO dw_user;
    ALTER DEFAULT PRIVILEGES IN SCHEMA intermediate GRANT ALL ON TABLES TO dw_user;
    ALTER DEFAULT PRIVILEGES IN SCHEMA marts GRANT ALL ON TABLES TO dw_user;
EOSQL

echo ">>> Data Warehouse 'vendas_dw' pronto (schemas: raw, staging, intermediate, marts)"
