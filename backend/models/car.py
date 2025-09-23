from sqlalchemy import Column, Integer, String

from models.base import Base

__all__ = [
    'Car',
]

class Car(Base):
    __tablename__ = 'car'
    id = Column(Integer, primary_key=True)
    brand = Column(String(255), nullable=False)
    model = Column(String(255), nullable=False)
    state_number = Column(String(20), nullable=False)
    vin = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
