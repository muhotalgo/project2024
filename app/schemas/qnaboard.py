from datetime import datetime

from pydantic import BaseModel


class QnaBoard(BaseModel):
    bno: int
    title: str
    userid: str
    # mno: int
    regdate: datetime
    # views: int
    contents: str

    class Config:
        from_attributes = True


class NewQna(BaseModel):
    title: str
    userid: str
    # mno: int
    contents: str
    response: str

# 정해진규칙에 데이터를 보내는지확인이 가능. models/board 에사용한 컬럼 이름이 동일해야함.