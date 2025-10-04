import pydantic


class BasePositionData(pydantic.BaseModel):
    is_work: bool
    title: str = pydantic.Field(max_length=255)
    unit: str = pydantic.Field(max_length=30)
    price: float
    in_stock_quantity: float
    using: bool = pydantic.Field(default=True)


class PositionData(BasePositionData):
    id: int


class WorkData(pydantic.BaseModel):
    id: int
    title: str = pydantic.Field(max_length=255)
    unit: str = pydantic.Field(max_length=30)
    price: float
    using: bool = pydantic.Field(default=True)
