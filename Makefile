# Environment detection
ENV ?= development

# Main run commands
.PHONY: run run-prod install clean frontend-install frontend-dev api dev lock

# Setup environment
setup-env:
	test -f .env || cp .env.example .env

setup-dev: setup-env
	# Other setup commands...

install: setup-env
	poetry install

# Frontend commands
frontend-install:
	cd frontend && npm install

frontend-dev: setup-env frontend-install
	cd frontend && npm run dev

# API commands
api: setup-env
	poetry run uvicorn app.api.main:app --reload --reload-exclude="frontend/*" --port 8000

api-prod: setup-env
	poetry run uvicorn app.api.main:app --port 8000

# Combined commands
run: install
ifeq ($(ENV),development)
	make -j2 api frontend-dev
else
	make -j2 api frontend-prod
endif

run-prod: ENV=production run

# Development tools
test:
	poetry run pytest

lint:
	poetry run flake8 .
	poetry run black .

clean:
	# Remove only node modules and build artifacts
	rm -rf frontend/node_modules
	rm -rf frontend/dist
	rm -rf app/frontend/node_modules
	rm -rf app/frontend/dist
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Add a new target for complete cleanup if needed
clean-all: clean
	rm -rf .venv

lock:
	poetry lock --no-update