.PHONY: install run test lint format clean lock

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