#!/bin/bash


# Ожидание запуска базы данных
echo "Waiting for database to be ready..."
while ! echo -e "\x1dclose\x0d" | telnet db 5432; do
  sleep 1
done

alembic upgrade head

gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 --reload
