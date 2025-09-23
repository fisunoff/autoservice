from sqlalchemy import Column, Integer, String

from models.base import Base

__all__ = [
    'Customer',
]

class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    patronymic = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
