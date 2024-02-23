from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from app.models.base import Base


class Qna(Base):
    __tablename__ = 'qna'
    qno = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(String(18), ForeignKey('member.userid'))
    # mno = Column(Integer, ForeignKey('member.mno'))
    title = Column(String(18), nullable=False)
    contents = Column(Text, nullable=False)
    regdate = Column(DateTime, default=datetime.now)

