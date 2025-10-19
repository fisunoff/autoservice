from collections import defaultdict

import pydantic
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import get_db
from models.car import Car
from schemas.car import CarData, BaseCarData
from utils.jwt_token import verify_token, verify_admin_role

car_router = APIRouter(
    tags=['Автомобиль'],
)


class CarOptionsResponse(pydantic.BaseModel):
    options: dict[str, list[str]]


@car_router.options('/', response_model=CarOptionsResponse)
async def get_car_options(
        db: AsyncSession = Depends(get_db),
        _token_payload: dict = Depends(verify_admin_role),
):
    """
    Возвращает словарь с опциями для создания/фильтрации машин.
    Ключи - бренды, значения - списки уникальных моделей для этого бренда.
    """
    stmt = select(Car.brand, Car.model).distinct().order_by(Car.brand, Car.model)

    results = (await db.execute(stmt)).all()

    options = defaultdict(list)
    for brand, model in results:
        options[brand].append(model)
    return {
        'options': options,
    }


@car_router.get('/', response_model=list[CarData])
async def get_cars(
        db: AsyncSession = Depends(get_db),
        _token_payload: dict = Depends(verify_admin_role),
) -> list[CarData]:
    """
    Список всех автомобилей.
    """
    stmt = select(Car)
    results = (await db.execute(stmt)).scalars().all()
    return results


@car_router.post('/', response_model=CarData)
async def create_car(
        data: BaseCarData,
        db: AsyncSession = Depends(get_db),
        _token_payload: dict = Depends(verify_admin_role),
):
    """
    Добавить автомобиль.
    """
    car = Car(**data.model_dump())
    db.add(car)
    await db.commit()
    await db.refresh(car)
    return car

# todo: детальный просмотр со связанным заказ-нарядами
