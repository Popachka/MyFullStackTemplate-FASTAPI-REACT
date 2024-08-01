#!/bin/sh
set -e

# Проверка на наличие аргумента
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <migration-message>"
  exit 1
fi

# Создание миграции с указанным сообщением
alembic revision --autogenerate -m "$1"
