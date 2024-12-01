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

docker-build:
	docker build -t lingograde .

docker-run:
	docker run -p 80:80 -p 8000:8000 \
		-e GOOGLE_CLOUD_PROJECT=silent-cider-443411-i4 \
		-e GOOGLE_CLOUD_REGION=us-central1 \
		-v $(PWD)/lingograde-stt-credentials.json:/app/lingograde-stt-credentials.json \
		lingograde

# Add a new development target
docker-run-dev:
	docker run -p 3000:3000 -p 8000:8000 \
		-e GOOGLE_CLOUD_PROJECT=silent-cider-443411-i4 \
		-e GOOGLE_CLOUD_REGION=us-central1 \
		-v $(PWD):/app \
		lingograde-dev npm run dev

# Add these new targets
docker-build-dev:
	docker build -t lingograde-dev -f Dockerfile.dev .

docker-run-dev: docker-build-dev
	docker run -p 3000:3000 -p 8000:8000 \
		-e GOOGLE_CLOUD_PROJECT=silent-cider-443411-i4 \
		-e GOOGLE_CLOUD_REGION=us-central1 \
		-v $(PWD):/app \
		lingograde-dev