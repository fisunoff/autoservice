from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

import models
from models import get_db, Position, Order
from schemas.order import OrderReadData, OrderCreate
from schemas.pricelist import PositionData, BasePositionData
from utils.jwt_token import verify_token, verify_admin_role

order_router = APIRouter(
    tags=['Заказ-наряды'],
)


@order_router.get('/', response_model=list[OrderReadData])
async def get_orders(
        db: AsyncSession = Depends(get_db),
        # _token: str = Depends(verify_token),
):
    stmt = (
        select(Order)
        .options(
            selectinload(Order.car),
            selectinload(Order.customer)
        )
    )
    orders = (await db.execute(stmt)).scalars().all()
    return orders


@order_router.post('/', response_model=OrderReadData)
async def create_order(
        order_data: OrderCreate,
        db: AsyncSession = Depends(get_db),
):
    car = await db.get(models.Car, order_data.car_id)
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Автомобиль с ID {order_data.car_id} не найден.'
        )
    customer = await db.get(models.Customer, order_data.customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Клиент с ID {order_data.customer_id} не найден."
        )

    db_order = models.Order(
        **order_data.model_dump(),
        car_given_out=False,
    )
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    db_order.car = car
    db_order.customer = customer
    return db_order
