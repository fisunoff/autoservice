import pydantic

__all__ = [
    'LeftOverData',
]


class LeftOverData(pydantic.BaseModel):
    id: int
    title: str = pydantic.Field(max_length=255)
    unit: str = pydantic.Field(max_length=30)
    price: float
    in_stock_quantity: float
    using: bool = pydantic.Field(default=True)
    last_month_usage: float = pydantic.Field(default=0.0)

    @pydantic.computed_field
    def need(self) -> float:
        if self.last_month_usage > 1 and self.last_month_usage > self.in_stock_quantity:
            return self.last_month_usage - self.in_stock_quantity
        return 0.0
