.PHONY: help build run stop test clean deploy

help:
	@echo "Available commands:"
	@echo "  make build    - Build Docker image"
	@echo "  make run      - Run with Docker Compose"
	@echo "  make stop     - Stop all containers"
	@echo "  make test     - Run tests"
	@echo "  make clean    - Remove all containers and images"
	@echo "  make deploy   - Deploy application"

build:
	docker build -t devops-platform:latest -f docker/Dockerfile .

run:
	cd docker && docker compose up -d

stop:
	cd docker && docker compose down

test:
	cd app && pip install -r requirements.txt && python -m pytest tests/ -v

clean:
	cd docker && docker compose down -v
	docker system prune -f

deploy:
	bash scripts/deploy.sh latest