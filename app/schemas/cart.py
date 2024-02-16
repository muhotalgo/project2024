from datetime import datetime

from pydantic import BaseModel


class Cart(BaseModel):
    cno: int
    quantity: int
    regdate: datetime
    userid: str
    pno: int

    class Config:
        from_attributes = True


class NewCart(BaseModel):
    quantity: int
    pno: int
