from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class Cart(Base):
    __tablename__ = 'cart'

    cno = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer, default=0)
    regdate = Column(DateTime, default=datetime.now)
    userid = Column(String(18), default=None)
    pno = Column(Integer, ForeignKey('product.pno'))