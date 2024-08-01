import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models.items import Item, ItemCreate, ItemPublic, ItemsPublic, ItemUpdate
from app.models.optional import Message
router = APIRouter()


@router.get('/', response_model=ItemsPublic)
def read_items(
    session: SessionDep, current_user: CurrentUser,
    skip: int = 0, limit: int = 100
) -> Any:
    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Item)
        count = session.exec(count_statement).one()
        statement = select(Item).offset(skip).limit(limit)
        items = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count()).select_from(Item).where(
                Item.owner_id == current_user.id
            )
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Item).where(Item.owner_id ==
                               current_user.id).offset(skip).limit(limit)

        )
        items = session.exec(statement).all()
    return ItemsPublic(data=items, count=count)


@router.delete('/{id}')
def delete_item(
    session: SessionDep, current_user: CurrentUser,
    id: uuid.UUID
) -> Message:
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404,
                            detail='Такого объекта не существует')
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(
            status_code=400,
            detail='Недостаточно привилегий'
        )
    session.delete(item)
    session.commit()
    return Message(message='Объект был удален')


@router.get('/{id}')
def read_item(
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID
) -> Any:
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404,
                            detail='Такого объекта не существует')
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(
            status_code=400,
            detail='Недостаточно привилегий'
        )
    return item


@router.post('/', response_model=ItemPublic)
def create_item(
    *, session: SessionDep, current_user: CurrentUser,
    item_in: ItemCreate
) -> Any:
    item = Item.model_validate(item_in, update={'owner_id': current_user.id})
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.put('/{id}', response_model=ItemPublic)
def update_item(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    item_in: ItemUpdate,
    id: uuid.UUID
) -> Any:
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404,
                            detail='Такого объекта не существует')
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(
            status_code=400,
            detail='Недостаточно привилегий'
        )
    update_dict = item_in.model_dump(exclude_unset=True)
    item.sqlmodel_update(update_dict)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item