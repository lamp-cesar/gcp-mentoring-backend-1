.PHONY: install run test lint format clean lock docker-build docker-run docker-run-detached docker-stop docker-logs docker-clean

install:
	poetry install

run:
	poetry run python main.py

test:
	poetry run pytest -q

lint:
	poetry run ruff check .

format:
	poetry run black .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf .venv

lock:
	poetry lock --no-update

# Docker targets
docker-build:
	docker build -t gcp-mentoring-backend:latest .

docker-run:
	docker run -p 8080:8080 \
		--env-file .env \
		--name gcp-mentoring-backend \
		gcp-mentoring-backend:latest

docker-run-detached:
	docker run -d -p 8080:8080 \
		--env-file .env \
		--name gcp-mentoring-backend \
		gcp-mentoring-backend:latest

docker-stop:
	docker stop gcp-mentoring-backend || true
	docker rm gcp-mentoring-backend || true

docker-logs:
	docker logs -f gcp-mentoring-backend

docker-clean:
	docker stop gcp-mentoring-backend || true
	docker rm gcp-mentoring-backend || true
	docker rmi gcp-mentoring-backend:latest || true