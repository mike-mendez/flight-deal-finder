from sqlmodel import Field, SQLModel, Column, ARRAY, JSON, String
from typing import Optional, Dict, List


# Data aggregated from Tequila
class DealBase(SQLModel):
    fly_from: str = Field(nullable=True)
    city_from: str = Field(nullable=True)
    fly_to: str = Field(nullable=True)
    city_to: str = Field(nullable=True)
    date_from: str = Field(nullable=True)
    date_to: str = Field(nullable=True)
    duration: Dict = Field(default={}, sa_column=Column(JSON), nullable=True)  # in seconds
    price: int = Field(nullable=True)
    airlines: List = Field(default=[], sa_column=Column(ARRAY(item_type=String)), nullable=True)
    url: str = Field(nullable=True)

    class Config:
        arbitrary_types_allowed = True


class Deal(DealBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class DealCreate(DealBase):
    pass


class DealRead(DealBase):
    id: int
