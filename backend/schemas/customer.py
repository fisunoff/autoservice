import pydantic

__all__ = [
    'BaseCustomerData',
    'CustomerData',
]

class BaseCustomerData(pydantic.BaseModel):
    name: str = pydantic.Field(max_length=255)
    surname: str = pydantic.Field(max_length=255)
    patronymic: str = pydantic.Field(max_length=255)
    phone: str = pydantic.Field(max_length=20)

class CustomerData(BaseCustomerData):
    id: int
