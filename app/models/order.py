from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from app.models.base import Base

class Order(Base):
    __tablename__ = 'order'

    ono = Column(Integer, primary_key=True, autoincrement=True)
    mno = Column(Integer, ForeignKey('member.mno'))
    status = Column(String(18), default='주문완료')
    unitprice = Column(Integer, default=0)
    quantity = Column(Integer, default=0)
    pdprice = Column(Integer, default=0)
    gono = Column(Integer, default=0)
    regdate = Column(DateTime, default=datetime.now)
    pno = Column(Integer, ForeignKey('product.pno'))
