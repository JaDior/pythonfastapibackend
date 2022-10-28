from typing import List
from pydantic import BaseModel
from src.schemas.tree_schema import *


class UserBase(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

    class Config:
        orm_mode = True


class UserInDB(UserBase):
    hashed_password: str


class User(UserBase):
    id: int
    trees: List[Tree] = []

    class Config:
        orm_mode = True
