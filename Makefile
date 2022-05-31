.PHONY: db-provision format-code migrate scripts shell start tests-run


db-provision:
	docker-compose run --rm app /bin/bash -c "python scripts/init_db.py"

format-code:
	docker-compose run --rm app /bin/bash -c "black -l 80 . && isort ."

migrate:
	docker-compose run --rm app /bin/bash -c "alembic upgrade head"

scripts:
	chmod +x bin/db-migrate

shell:
	docker-compose run --rm app /bin/bash

start:
	docker-compose up -d

tests-run:
	docker-compose run --rm app-tests


