from datetime import datetime

from pydantic import BaseModel


class Member(BaseModel):
    mno: int
    userid: str
    passwd: str
    zipcode: int
    address: str
    address2: str
    name: str
    phone: int
    email: str
    regdate: datetime

    class Config:
        from_attributes = True


class NewMember(BaseModel):
    userid: str
    passwd: str
    name: str
    email: str
