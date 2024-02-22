from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

class Qna(Base):
    __tablename__ = 'qna'
    qno = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(String(18), nullable=False)
    title = Column(String(18), nullable=False)
    contents = Column(Text, nullable=False)
    regdate = Column(DateTime, default=datetime.now)

