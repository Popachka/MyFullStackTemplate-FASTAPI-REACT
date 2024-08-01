import uuid
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional, Union

class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=255)

class ItemCreate(ItemBase):
    title: str = Field(min_length=1, max_length=255)
class ItemUpdate(ItemBase):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
class Item(ItemBase, table = True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: uuid.UUID = Field(foreign_key='user.id', nullable=False)
    owner: Optional["User"] = Relationship(back_populates='items')
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID
class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int
