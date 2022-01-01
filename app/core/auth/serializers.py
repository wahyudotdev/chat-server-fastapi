from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    id: str
    name: Optional[str] = None
    username: str
    email: str
    created: datetime
    updated: datetime
    photo: Optional[str]
    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []
