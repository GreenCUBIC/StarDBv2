#! /bin/bash
docker exec -it stardb2-database psql -U stardb_admin -p 5556 -c "CREATE DATABASE development;"
docker exec -it stardb2-database psql -U stardb_admin -p 5556 -c "CREATE DATABASE estrous_cycle;"
docker exec -it stardb2-database /app/data/development/restore_dump.sh
docker exec -it stardb2-database /app/data/estrous_cycle/restore_dump.sh
