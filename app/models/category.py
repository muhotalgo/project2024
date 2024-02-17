from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.models.cart import Base


class Category(Base):
    __tablename__ = 'category'

    ctno = Column(Integer, primary_key=True, autoincrement=True)
    kctname = Column(String(18), nullable=False)
    sctname = Column(String(18), nullable=False)
    catcod = Column(Integer, nullable=False, unique=True)
    regdate = Column(DateTime, default=datetime.now)
    products = relationship("Product", backref="category.ctno")
