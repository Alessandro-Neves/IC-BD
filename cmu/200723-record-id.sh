make postgres

docker exec -it ic-db-postgres bash
psql -U root -h localhost -p 5432
\! clear