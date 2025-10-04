from sqlalchemy import Column, Integer, ForeignKey, Float, Computed
from sqlalchemy.orm import mapped_column, relationship

from models.base import Base


class DetailUsage(Base):
    __tablename__ = 'detail_usage'
    id = Column(Integer, primary_key=True)
    order_id = mapped_column(ForeignKey('orders.id', ondelete='RESTRICT'), nullable=False)
    order = relationship('Order', back_populates='details')
    position_id = mapped_column(ForeignKey('pricelist.id', ondelete='RESTRICT'), nullable=False)
    position = relationship('Position')
    price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    cost = Column(Float, Computed('price * quantity', persisted=True))
