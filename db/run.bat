@echo off
docker run --network retail-data-net -p 5432:5432 --name retail-database -e POSTGRES_PASSWORD=1234 -e POSTGRES_USER=retail-data -d postgres