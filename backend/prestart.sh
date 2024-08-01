#! /usr/bin/env bash
alembic revision --autogenerate -m "Initial migration"

alembic upgrade head

python /app/app/initial_data.py
