.PHONY: help install dev-install test lint format clean docker-build docker-up docker-down

help:
	@echo "Available commands:"
	@echo "  install      Install production dependencies"
	@echo "  dev-install Install development dependencies"
	@echo "  test        Run tests"
	@echo "  lint        Run linting"
	@echo "  format      Format code"
	@echo "  clean       Clean up temporary files"
	@echo "  docker-build Build Docker images"
	@echo "  docker-up   Start Docker containers"
	@echo "  docker-down Stop Docker containers"

install:
	cd frontend && npm install --production

dev-install:
	cd frontend && npm install
	pre-commit install

test:
	docker compose exec backend pytest
	cd frontend && npm test

lint:
	docker compose exec backend flake8 app tests
	cd frontend && npm run lint

format:
	docker compose exec backend black app tests
	cd frontend && npm run format

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".coverage" -exec rm -r {} +
	find . -type d -name "node_modules" -exec rm -r {} +
	find . -type d -name "build" -exec rm -r {} +
	find . -type d -name "dist" -exec rm -r {} +
	find . -type d -name "venv" -exec rm -r {} +

docker-build:
	docker compose build

docker-up:
	docker compose up -d

docker-down:
	docker compose down
