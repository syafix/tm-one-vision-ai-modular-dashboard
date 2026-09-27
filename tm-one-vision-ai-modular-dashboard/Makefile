.PHONY: up down logs test seed lint
up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f api web

test:
	docker compose exec api pytest

seed:
	docker compose exec api python -m app.seed

lint:
	docker compose exec api ruff check app tests
