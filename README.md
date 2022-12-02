# simple_search_app

## local deployment
For local deploying use docker-compose.yaml file

## test running
First docker-compose services should be running in Docker + local venv

## for migrations
yoyo apply --database postgresql://postgres:postgres@0.0.0.0:5432/postgres ../migrations -b
