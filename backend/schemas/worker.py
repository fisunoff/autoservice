import datetime

import pydantic

__all__ = [
    'BaseWorkerData',
    'ReadWorkerData',
    'ProfileCreate',
]

class BaseWorkerData(pydantic.BaseModel):
    name: str = pydantic.Field(max_length=255)
    surname: str = pydantic.Field(max_length=255)
    patronymic: str = pydantic.Field(max_length=255)
    tabel_number: str = pydantic.Field(max_length=20)
    hire_date: datetime.date


class ReadWorkerData(BaseWorkerData):
    id: int
    is_admin: bool
    is_mechanic: bool
    is_active: bool
    login: str
    fire_date: datetime.date

class ProfileCreate(BaseWorkerData):
    is_admin: bool
    is_mechanic: bool
    is_active: bool
    login: str
    password: str
