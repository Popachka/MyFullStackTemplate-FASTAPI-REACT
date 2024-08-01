import uuid
from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app import crud
from app.core.config import settings
from app.core.security import verify_password
from app.models.user import User, UserCreate
from app.tests.utils.utils import random_email, random_lower_string

def test_get_users_superuser_me(
        client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    curr_user = r.json()
    assert curr_user
    assert curr_user['is_active'] is True
    assert curr_user['is_superuser']
    assert curr_user['email'] == settings.FIRST_SUPERUSER