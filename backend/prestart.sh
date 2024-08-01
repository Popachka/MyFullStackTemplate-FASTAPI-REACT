#! /usr/bin/env bash
RUN alembic revision --autogenerate -m "Initial migration"

alembic upgrade head

python /app/app/initial_data.py
