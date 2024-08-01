FROM python:3.9-slim-buster

WORKDIR /app

# Установить зависимости
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PYTHONPATH=/app

# Копировать исходный код и скрипты
COPY ./app /app/app
COPY ./prestart.sh /app/
COPY ./alembic.ini /app/
COPY ./scripts/ /app/
COPY ./tests-start.sh /app/
COPY ./start-reload.sh /
COPY ./clear_bd.sh /app/
COPY ./create_migrate.sh /app/  
COPY ./migrate.sh /app/  


# Установить права на выполнение для скриптов
RUN chmod +x /start-reload.sh
