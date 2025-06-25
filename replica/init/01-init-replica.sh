#!/bin/bash
set -e

# Wait for primary to be ready
PGPASSWORD=postgres
until pg_isready -h pg-primary  -d postgres ; do
  echo "Waiting for primary..."
  sleep 2
done

# Wipe existing data
rm -rf "$PGDATA"/*

# Perform base backup from primary
PGPASSWORD=replpass pg_basebackup -h pg-primary -D "$PGDATA" -U replicator -Fp -Xs -P -R

# Adjust permissions
chown -R postgres:postgres "$PGDATA"

