from datetime import datetime

from pydantic import BaseModel


class Category(BaseModel):
    ctno: int
    kctname: str
    sctname: str
    catcod: int
    regdate: datetime

    class Config:
        from_attributes = True


class NewCategory(BaseModel):
    kctname: str
    sctname: str
    catcod: int