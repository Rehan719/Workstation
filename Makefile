.PHONY: setup build test deploy-local clean backup restore

setup:
	@echo "Setting up environment..."
	pip install poetry
	poetry install
	./scripts/init-secrets.sh
	@echo "Setup complete. Please edit .env to add your API keys."

build:
	@echo "Building Docker images..."
	docker-compose -f infra/docker/docker-compose.yml build

test:
	@echo "Running tests..."
	poetry run pytest tests/

deploy-local:
	@echo "Starting local deployment..."
	docker-compose -f infra/docker/docker-compose.yml up -d

clean:
	@echo "Stopping containers and cleaning up..."
	docker-compose -f infra/docker/docker-compose.yml down -v

backup:
	@echo "Creating backup..."
	./scripts/backup.sh

restore:
	@echo "Restoring from backup..."
	./scripts/restore.sh
