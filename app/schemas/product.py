from datetime import datetime

from pydantic import BaseModel


class Product(BaseModel):
    prodno: int
    name: str
    exp: str
    detail: str
    retail: str
    price: str
    pctoff: str
    useyn: str
    tumbimg: str
    stock: int
    width: int
    deps: int
    height: int
    color: str
    regdate: datetime
    catnum: int

    class Config:
        from_attributes = True


class NewProduct(BaseModel):
    name: str
    exp: str
    detail: str
    retail: str
    pctoff: str
    useyn: str
    tumbimg: str
    stock: int
    width: int
    deps: int
    height: int
    color: str
    catnum: int