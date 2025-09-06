#!/bin/bash
set -e

APP_MODULE="app:app"          # points to app.py and FastAPI instance "app"
HOST="0.0.0.0"
PORT=${PORT:-8000}            # Render assigns $PORT dynamically
WORKERS=1                     

echo "Starting FastAPI on port $PORT..."
exec gunicorn $APP_MODULE \
    -k uvicorn.workers.UvicornWorker \
    --workers $WORKERS \
    --bind $HOST:$PORT \
    --timeout 120

