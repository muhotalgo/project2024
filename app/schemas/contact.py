# from datetime import datetime
#
# from pydantic import BaseModel
#
#
# class Notice(BaseModel):
#     gno: int
#     regdate: datetime
#     title: str
#     contents: str
#     class Config:
#         from_attributes = True




from datetime import datetime

from pydantic import BaseModel

class Qna(BaseModel):
    qno: int
    userid: str
    title: str
    contents: int
    regdate: datetime
    class Config:
        from_attributes = True

class Notice(BaseModel):
    nno: int
    title: str
    regdate: datetime
    views: int
    contents: str
    class Config:
        from_attributes = True

