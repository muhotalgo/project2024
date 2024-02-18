from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from app.models.cart import Cart

class Base(DeclarativeBase):
    pass


class Order(Base):
    __tablename__ = 'order'

    ono = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(String(18), nullable=False)
    status = Column(String(18), nullable=False)
    unitprice = Column(Integer, default=0)
    regdate = Column(DateTime, default=datetime.now)
    ino = Column(Integer, ForeignKey('orderitem.ino'))


class OrderItem(Base):
    __tablename__ = 'orderitem'

    ino = Column(Integer, primary_key=True, autoincrement=True)
    regdate = Column(DateTime, default=datetime.now)