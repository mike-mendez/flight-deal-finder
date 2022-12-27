from pydantic import Extra
from sqlmodel import Field, SQLModel
from typing import Optional


class TestBase(SQLModel):
    city: str = Field(unique=True, nullable=False)
    lowest_price: int = Field(nullable=False)


class Test(TestBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    iata_code: str = Field(unique=True, nullable=False)


class TestCreate(TestBase):
    pass

    class Config:
        extra = Extra.allow


class TestRead(TestBase):
    id: int
    iata_code: str
