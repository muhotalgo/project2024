from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base


class Member(Base):
    __tablename__ = 'member'

    mno = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(String(18), nullable=False, unique=True)
    passwd = Column(String(18), nullable=False)
    zipcode = Column(String(5), nullable=False)
    address1 = Column(String(100), nullable=False)
    address2 = Column(String(100), nullable=False)
    name = Column(String(20), nullable=False)
    phone = Column(String(11), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    regdate = Column(DateTime, default=datetime.now)
    qna = relationship("Qna", backref="member.userid")  # 수정: backref="member"
    contact = relationship("Contact", backref="member.userid")  # 수정: backref="member"
    boards = relationship("Board", backref="member.userid")
    orders = relationship("Order", backref="member.mno")







