from sqlalchemy import Column, Integer, Boolean, String, Float

from models import Base


class Position(Base):
    __tablename__ = 'pricelist'
    id = Column(Integer, primary_key=True)
    is_work = Column(Boolean)  # если не работа, то деталь
    title = Column(String(255), nullable=False)
    unit = Column(String(30), nullable=False)
    price = Column(Float)
    in_stock_quantity = Column(Float)
    using = Column(Boolean)  # используется ли
