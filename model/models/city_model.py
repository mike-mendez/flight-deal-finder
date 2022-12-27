# from sqlmodel import Field, SQLModel
# from typing import Optional
#
#
# class CityBase(SQLModel):
#     flyFrom: "FRA",
#     flyTo: "PRG",
#     cityFrom: "Frankfurt",
#     cityCodeFrom: "FRA",
#     cityTo: "Prague",
#     cityCodeTo: "PRG",
#     nights_in_destination:
#     duration:
#     quality:
#     price:
#     fare: list
#     bags_price
#     availability: dict
#     deep_link:
#
#
#
#
#     original_query: str
#
#
# class City(CityBase, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#
#
# class CityCreate(CityBase):
#     pass
#
#
# class CityRead(CityBase):
#     pass
