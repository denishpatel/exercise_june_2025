#!/bin/bash
echo "host replication replicator all md5" >> "$PGDATA/pg_hba.conf"
echo "wal_level = replica" >> "$PGDATA/postgresql.conf"
echo "max_wal_senders = 10" >> "$PGDATA/postgresql.conf"
echo "hot_standby = on" >> "$PGDATA/postgresql.conf"
