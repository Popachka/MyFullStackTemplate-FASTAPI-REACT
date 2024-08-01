from sqlmodel import SQLModel
from typing import Union

class Token(SQLModel):
    access_token: str
    token_type: str = 'bearer'
class TokenPayload(SQLModel):
    sub: Union[str,None] = None

class Message(SQLModel):
    message: str