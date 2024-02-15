from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = 'product'

    prodno = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(18), nullable=False)
    exp = Column(String(50), default=None)
    detail = Column(String(500), default=None)
    retail = Column(Integer, nullable=False)
    price = Column(Integer, default=0)
    pctoff = Column(Integer, default=0)
    useyn = Column(String(18), default='y')
    tumbimg = Column(String(50), default=None)
    regdate = Column(DateTime, default=datetime.now)
    stock = Column(Integer, default=0)
    width = Column(Integer, default=0)
    deps = Column(Integer, default=0)
    height = Column(Integer, default=0)
    color = Column(String(18), default=None)
    catnum = Column(Integer, default=0)