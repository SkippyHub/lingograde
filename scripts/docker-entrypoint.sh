#!/bin/bash
set -e

if [ "$1" = "debug" ]; then
    echo "Starting in debug mode..."
    python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m streamlit run app/main.py --server.address 0.0.0.0
else
    exec "$@"
fi 