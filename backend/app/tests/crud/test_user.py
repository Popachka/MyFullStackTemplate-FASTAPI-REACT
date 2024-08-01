from sqlmodel import Session
from app.tests.utils.utils import random_lower_string, random_email
from app import crud
from app.core.security import verify_password
from app.models.user import UserCreate

def test_create_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.create_user(session = db, user_create=user_in)
    assert user.email == email
    assert hasattr(user, 'hashed_password')

def test_authenticate_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.create_user(session=db, user_create=user_in)
    auth_user = crud.authenticate(session=db, email=email, password=password)
    assert auth_user
    assert user.email == auth_user.email