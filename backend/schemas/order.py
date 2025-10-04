import datetime

import pydantic
from pydantic import Field

from schemas.car import CarData
from schemas.customer import CustomerData
from schemas.pricelist import PositionData


class OrderCreate(pydantic.BaseModel):
    customer_id: int
    car_id: int
    car_received: bool
    opened_date: datetime.date = Field(default_factory=datetime.date.today)


class OrderReadData(pydantic.BaseModel):
    id: int
    customer: CustomerData
    car: CarData
    car_received: bool
    car_given_out: bool
    paid_date: datetime.date | None
    opened_date: datetime.date
    closed_date: datetime.date | None


class DetailUsageForOrder(pydantic.BaseModel):
    position: PositionData
    price: float
    quantity: float
    cost: float


class OrderDetailData(OrderReadData):
    details: list[DetailUsageForOrder]
