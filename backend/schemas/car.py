import pydantic

__all__ = [
    'BaseCarData',
    'CarData',
]

class BaseCarData(pydantic.BaseModel):
    brand: str = pydantic.Field(max_length=255)
    model: str = pydantic.Field(max_length=255)
    state_number: str = pydantic.Field(max_length=20)
    vin: str = pydantic.Field(max_length=50)
    year: int = pydantic.Field(gt=1800)

class CarData(BaseCarData):
    id: int
