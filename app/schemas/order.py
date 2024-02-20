from datetime import datetime
from typing import List

from pydantic import BaseModel


class Order(BaseModel):
    ono: int
    mno: int
    status: str
    unitprice: int
    pno: int
    quantity: int
    pdprice: int
    regdate: datetime

    class Config:
        from_attributes = True


class NewOrder(BaseModel):
    mno: int
    status: str
    unitprice: int
    pno: int
    quantity: int
    pdprice: int


class NewOrders(BaseModel):
    order: List[NewOrder]
