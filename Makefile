.PHONY: venv install install-dev run test lint clean frontend-install frontend-dev api dev

# Detect OS
ifeq ($(OS),Windows_NT)
	PYTHON_PATH := $(shell where python)
	VENV_BIN := venv/Scripts
else
	PYTHON_PATH := $(shell which python3)
	VENV_BIN := venv/bin
endif

# Check if pyenv is available
PYENV_PATH := $(shell command -v pyenv 2> /dev/null || where pyenv 2> /dev/null)
ifdef PYENV_PATH
	ifeq ($(OS),Windows_NT)
		PYTHON_PATH := $(shell pyenv prefix 3.11.7)/python
	else
		PYTHON_PATH := $(shell pyenv prefix 3.11.7)/bin/python
	endif
endif

venv:
	$(PYTHON_PATH) -m venv venv

install: venv
	. venv/bin/activate && pip install --upgrade pip
	. venv/bin/activate && pip install -r requirements.txt

install-dev: install
	. venv/bin/activate && pip install -r requirements-dev.txt

run: venv
	. venv/bin/activate && python -m streamlit run app/main.py

test: venv
	. venv/bin/activate && python -m pytest

lint: venv
	. venv/bin/activate && python -m flake8 .
	. venv/bin/activate && python -m black .

clean:
	rm -rf venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Frontend commands
frontend-install:
	cd frontend && npm install

frontend-dev:
	cd frontend && npm run dev

# API commands
api:
	. venv/bin/activate && uvicorn app.api.main:app --reload --port 8000

# Combined commands
dev: install
	make -j2 api frontend-dev