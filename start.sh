#!/bin/bash
set -e

APP_MODULE="app:app"
HOST="0.0.0.0"
PORT="8000"
WORKERS=4

echo "Starting FastAPI with Gunicorn + Uvicorn workers..."
exec gunicorn $APP_MODULE \
    -k uvicorn.workers.UvicornWorker \
    --workers $WORKERS \
    --bind $HOST:$PORT \
    --timeout 120
