#!/bin/bash
set -e

# delete containers
docker rm -f pg-primary
docker rm -f pg-replica
# Remove volumes
docker volume remove -f exercise_june_2025_pg-replica-data
docker volume remove -f exercise_june_2025_pg-primary-data
