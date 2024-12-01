#!/bin/bash

# Start the Python backend in the background
poetry run uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload &

# Change to frontend directory and start development server
cd frontend && /app/frontend/node_modules/.bin/vite --host 0.0.0.0