#!/bin/bash
set -e

APP_MODULE="app:app"         
HOST="0.0.0.0"
PORT=${PORT:-8000}         

echo "Starting FastAPI with Uvicorn..."
exec uvicorn $APP_MODULE --host $HOST --port $PORT --workers 1

