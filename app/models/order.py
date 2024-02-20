from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from app.models.cart import Cart

class Base(DeclarativeBase):
    pass


class Order(Base):
    __tablename__ = 'order'

    ono = Column(Integer, primary_key=True, autoincrement=True)
    mno = Column(Integer, default=0)
    # mno = Column(Integer, ForeignKey('member.pno'))
    status = Column(String(18), default='주문완료')
    unitprice = Column(Integer, default=0)
    pno = Column(Integer, default=0)
    # pno = Column(Integer, ForeignKey('product.pno'))
    quantity = Column(Integer, default=0)
    pdprice = Column(Integer, default=0)
    regdate = Column(DateTime, default=datetime.now)
