#! /bin/bash
docker exec -it stardb2-database-1 /app/data/development/generate_dump.sh
docker exec -it stardb2-database-1 /app/data/estrous_cycle/generate_dump.sh