from datetime import datetime

from pydantic import BaseModel


class Member(BaseModel):
    mno: int
    userid: str
    passwd: str
    zipcode: str
    address1: str
    address2: str
    name: str
    phone: str
    email: str
    regdate: datetime

    class Config:
        from_attributes = True


class NewMember(BaseModel):
    userid: str
    passwd: str
    zipcode: str
    address1: str
    address2: str
    name: str
    phone: str
    email: str
