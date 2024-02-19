from datetime import datetime

from pydantic import BaseModel


class Order(BaseModel):
    ono: int
    userid: str
    status: str
    unitprice: int
    regdate: datetime
    ino: int

    class Config:
        from_attributes = True


class NewOrder(BaseModel):
    pass


class OrderItem(BaseModel):
    ino: int
    pno: int
    quantity: int
    pdprice: int
    unitno: int
    regdate: str

    class Config:
        from_attributes = True


class NewOrderItem(BaseModel):
    pno: int
    quantity: int
    pdprice: int
    unitno: int
