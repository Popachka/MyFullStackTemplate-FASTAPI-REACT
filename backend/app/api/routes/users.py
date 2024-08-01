from app.core.config import settings
from typing import Any
from sqlmodel import col, delete, func, select

from app.core.security import get_password_hash, verify_password
from app.models.user import (
    User,
    UserCreate,
    UserRegister,
    UserUpdate,
    UserUpdateMe,
    UserPublic,
    UpdatePassword
)
from app.models.optional import Message
from app import crud
from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import (
    get_current_active_superuser,
    SessionDep,
    CurrentUser
)
import uuid

router = APIRouter()


@router.get(
    '/',
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserPublic
)
def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    print('--------------------hello')
    count_statement = select(func.count()).select_from(User)
    count = session.exec(count_statement).one()

    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()

    return UserPublic(data=users, count=count)


@router.post(
    '/',
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserPublic
)
def create_user(*, session: SessionDep, user_in: UserCreate) -> Any:
    print('create_use')
    user = crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail='Пользователь с таким Email уже существует'
        )
    user = crud.create_user(session=session, user_create=user_in)

    return user


@router.post('/signup', response_model=UserPublic)
def register_user(session: SessionDep, user_in: UserRegister) -> Any:

    user = crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail='Пользователь с таким Email уже существует'
        )
    user_create = UserCreate.model_validate(user_in)
    user = crud.create_user(session=session, user_create=user_create)
    return user


@router.get('/me', response_model=UserPublic)
def read_user_me(current_user: CurrentUser) -> Any:
    return current_user


@router.patch("/me", response_model=UserPublic)
def update_user_me(*, session: SessionDep, user_in: UserUpdateMe,
                   current_user: CurrentUser) -> Any:
    if user_in.email:
        existing_user = crud.get_user_by_email(
            session=session, email=user_in.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=409,
                detail='Пользователь с таким email-ом уже существует'
            )
    user_data = user_in.model_dump(exclude_unset=True)
    current_user.sqlmodel_update(user_data)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user


@router.patch('/me/password', response_model=Message)
def update_password_me(
    *, session: SessionDep, body: UpdatePassword, current_user: CurrentUser
) -> Any:
    if not verify_password(body.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail='Неправильный пароль')
    if body.current_password == body.new_password:
        raise HTTPException(
            status_code=400, detail="Новый пароль не может совпадать с текущим"
        )
    hashed_pass = get_password_hash(body.new_password)
    current_user.hashed_password = hashed_pass
    session.add(current_user)
    session.commit()
    return Message(message='Пароль успешно изменен')

@router.get('/{user_id}', response_model=UserPublic)
def read_user_by_id(
    user_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser
) -> Any:
    user = session.get(User, user_id)
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail='Вы не имеете достаточно привилегий'
        )
    return user

@router.delete('/me', response_model=Message)
def delete_user_me(session: SessionDep, current_user: CurrentUser) -> Any:
    if current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail='Суперпользователь не может быть удален'
        )
    session.delete(current_user)
    session.commit()
    return Message(message='Пользователь успешно удален')
@router.delete('/{user_id}', dependencies=[Depends(get_current_active_superuser)])
def delete_user(session: SessionDep, current_user: CurrentUser, user_id: uuid.UUID) -> Message:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    if user == current_user:
        raise HTTPException(
            status_code=403,
            detail='Суперпользователь не может быть удален'
        )
    session.delete(user)
    session.commit()
    return Message(message='Пользователь успешно удален')