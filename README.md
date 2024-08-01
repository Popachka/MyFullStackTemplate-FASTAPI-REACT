# Мой базовый шаблон для проекта на FastAPI + React(пока не реализован)

Это шаблон, основанный на известном [шаблоне](https://github.com/Popachka/full-stack-fastapi-template) от создателя FastAPI>, но я его изменил под себя, чтобы я смог с ним удобно работать. Так что, если вам нужен исходник то еще раз [вот](https://github.com/Popachka/full-stack-fastapi-template)

Сейчас шаблон выполнен только для локальный разработки backend сервисов. Планируется доделать и для продакшн среды и добавить React, как фронтенд

# Технологии, которые я использовал

- [**FastAPI**](https://fastapi.tiangolo.com) Python backend
    - [SQLModel](https://sqlmodel.tiangolo.com) Хорошая ORM, удобная
    как раз для FastAPI
    - [Pydantic](https://docs.pydantic.dev) Вся валидация данных и найстройки проекта держатся на этой библиотеке
    - [PostgreSQL](https://www.postgresql.org) SQL база данных
    - [Alembic](https://alembic.sqlalchemy.org/en/latest/index.html) Миграции и версионирование бд
- [Docker Compose](https://www.docker.com) для развертывания контейнеров в деплое. Вся работа протекает через контнейнеры.

- Настроены JWT для авторизации
- Тестируется python код через библиотеку: [Pytest](https://pytest.org)


# Чтобы использовать этот шаблон в данный момент надо:

- fork or clone этот репозиторий 

```bash
git clone https://github.com/Popachka/MyFullStackTemplate-FASTAPI-REACT.git
```

- Войдите в шаблон

```bash
cd MyFullStackTemplate-FASTAPI-REACT
```

### Конфигурация и .env файл

Прежде чем запускать шаблон, ознакомьтесь с переменными среды и установите ваши значения, которые вам будут удобны.

# Backend Development

Backend docs: [backend/README.md](./backend/README.md).