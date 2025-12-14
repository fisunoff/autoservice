from sqlalchemy import Column, Integer, String, Boolean, Date

from models.base import Base
from sqlalchemy.orm import relationship

__all__ = [
    'Profile',
]


class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    patronymic = Column(String(255), nullable=False)
    tabel_number = Column(String(20), nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    is_mechanic = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
    hire_date = Column(Date, nullable=True)
    fire_date = Column(Date, nullable=True)
    login = Column(String(255), nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    orders_by_mechanic = relationship('Order',  foreign_keys='[Order.responsible_mechanic_id]', back_populates='responsible_mechanic')
    orders_by_admin = relationship('Order', foreign_keys='[Order.responsible_admin_id]', back_populates='responsible_admin')
