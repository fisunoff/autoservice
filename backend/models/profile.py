from sqlalchemy import Column, Integer, String, Boolean

from models.base import Base

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
    login = Column(String(255), nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
