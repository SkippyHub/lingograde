.PHONY: venv install install-dev run test lint clean

# Detect OS
ifeq ($(OS),Windows_NT)
	PYTHON_PATH := $(shell where python)
	VENV_BIN := venv/Scripts
else
	PYTHON_PATH := $(shell which python3)
	VENV_BIN := venv/bin
endif

# Check if pyenv is available
PYENV_PATH := $(shell command -v pyenv 2> /dev/null)
ifdef PYENV_PATH
	PYTHON_PATH := $(HOME)/.pyenv/versions/3.11.7/bin/python
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