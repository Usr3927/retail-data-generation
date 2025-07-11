@echo off
docker run --network retail-data-net --name retail_data_gen --rm --mount type=bind,source=".\code",target=/local python-docker /local/run.sh