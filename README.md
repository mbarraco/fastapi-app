# Tasks API

An API for managing Tasks (and creating Users). 

This project runs on [FastAPI](https://fastapi.tiangolo.com/) + [Sqlaclhemy](https://www.sqlalchemy.org/) + [Alembic](https://alembic.sqlalchemy.org/en/latest/)


## Requirements

* Unix-like OS
* Docker (please check [docker-compose.yml](docker-compose.yml) version)

## Port usage 
(see [docker-compose.yml](docker-compose.yml))
* Server will run on `localhost:8079`
* Database will run on port `5432`

## API setup

1.  Rename `.env.example` to `.env`. This should be enought to work with this system out of the shelf.

From project's root (where Makefile is located):

2. run `make start`
3. run `make db-provision`
4. run `make migrate`

## API docs

A Swagger documentation service can be accessed at [localhost:8079/docs](localhost:8079/docs)

A Postman collection is included in [project/postman_collection.json](postman_collection.json)

## Tests
Integration tests are provided, run with:

`make tests-run`

Tests will run on a dedicated `docker-compose` service.

## Future work

1. Unit tests
2. API layer use db as context manager
3. Improve integration test run platform
