from sqlalchemy import Column, Integer, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship, mapped_column

import models

__all__ = [
    'Order',
]


class Order(models.Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    customer_id = mapped_column(ForeignKey('customer.id', ondelete='RESTRICT'), nullable=False)
    customer = relationship('Customer', back_populates='orders')
    car_id = mapped_column(ForeignKey('car.id', ondelete='RESTRICT'), nullable=False)
    car = relationship('Car', back_populates='orders')
    car_received = Column(Boolean, nullable=False)  # получен
    car_given_out = Column(Boolean, nullable=False)  # выдан
    paid_date = Column(Date, nullable=True)  # дата оплаты
    opened_date = Column(Date, nullable=False)  # дата открытия
    closed_date = Column(Date, nullable=True)  # дата закрытия
