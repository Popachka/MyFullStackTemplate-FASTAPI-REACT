#!/bin/sh
set -e

# Применение миграций при запуске контейнера
alembic upgrade head

# Запуск Uvicorn с автообновлением
exec uvicorn app.main:app --host 0.0.0.0 --port 8888 --reload
