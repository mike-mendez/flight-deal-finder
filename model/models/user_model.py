from datetime import datetime
from sqlmodel import Field, SQLModel
from typing import Optional


# Definition for User model
class UserBase(SQLModel):
    username: str = Field(unique=True, nullable=False, index=True)
    email: str = Field(unique=True, nullable=False, index=True)
    password: str = Field(nullable=False)


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    data_created: Optional[str] = Field(default=datetime.utcnow(), nullable=False)
    is_active: Optional[bool] = Field(default=True)


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    pass
