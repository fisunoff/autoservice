import datetime

import pydantic
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

import models
from models import get_db, Order, DetailUsage, WorkUsage, Profile
from schemas.order import OrderReadData, OrderCreate, OrderDetailData
from utils.jwt_token import verify_token, verify_admin_role

order_router = APIRouter(
    tags=['Заказ-наряды'],
)


async def get_prefetched_order(pk: int, db: AsyncSession) -> Order | None:
    order_stmt = (
        select(Order)
        .options(
            selectinload(Order.car),
            selectinload(Order.customer),
            selectinload(Order.details).selectinload(DetailUsage.position),
            selectinload(Order.works).selectinload(WorkUsage.position),
        )
        .where(Order.id == pk)
    )
    order = (await db.execute(order_stmt)).scalars().first()
    return order


@order_router.get('/', response_model=list[OrderReadData])
async def get_orders(
        db: AsyncSession = Depends(get_db),
        _token: str = Depends(verify_token),
):
    stmt = (
        select(Order)
        .options(
            selectinload(Order.car),
            selectinload(Order.customer),
        )
    )
    orders = (await db.execute(stmt)).scalars().all()
    return orders


@order_router.get('/{pk}', response_model=OrderDetailData)
async def get_order(
        pk: int,
        db: AsyncSession = Depends(get_db),
        _token: str = Depends(verify_token),
):
    """
    Детальная информация по заказ-наряду.
    """
    order = await get_prefetched_order(pk, db)
    if not order:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return order


@order_router.post('/{pk}/set_paid', response_model=OrderDetailData)
async def set_paid(
        pk: int,
        db: AsyncSession = Depends(get_db),
        _token: str = Depends(verify_admin_role),
):
    """
    Указать, что заказ-наряд оплачен. Только для администратора.
    """
    order = await get_prefetched_order(pk, db)
    if not order:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    if order.paid_date or order.closed_date:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='Невозможно перевести заказ в статус Оплачен')
    order.paid_date = datetime.datetime.now().date()
    db.add(order)
    await db.commit()
    return order


@order_router.post('/{pk}/set_responsible_admin/{admin_pk}/', response_model=OrderDetailData)
async def set_responsible_admin(
        pk: int,
        admin_pk: int,
        db: AsyncSession = Depends(get_db),
        _token: str = Depends(verify_admin_role),
):
    """
    Назначить ответственного администратора. Только для администратора.
    """
    order = await get_prefetched_order(pk, db)
    if not order:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    admin = await db.get(Profile, admin_pk)
    if not admin:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    if not admin.is_admin:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail='Назначаемый пользователь не обладает правами администратора',
        )
    if not admin.is_active:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail='Назначаемый пользователь не активен',
        )
    order.responsible_admin_id = admin.id
    db.add(order)
    await db.commit()
    return order


@order_router.post('/{pk}/set_responsible_mechanic/{mechanic_pk}/', response_model=OrderDetailData)
async def set_responsible_admin(
        pk: int,
        mechanic_pk: int,
        db: AsyncSession = Depends(get_db),
        _token: str = Depends(verify_admin_role),
):
    """
    Назначить ответственного механика. Только для администратора.
    """
    order = await get_prefetched_order(pk, db)
    if not order:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    mechanic = await db.get(Profile, mechanic_pk)
    if not mechanic:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    if not mechanic.is_mechanic:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail='Назначаемый пользователь не обладает правами механика',
        )
    if not mechanic.is_active:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail='Назначаемый пользователь не активен',
        )
    order.responsible_mechanic_id = mechanic.id
    db.add(order)
    await db.commit()
    return order


@order_router.post('/{pk}/close', response_model=OrderDetailData)
async def close_order(
        pk: int,
        db: AsyncSession = Depends(get_db),
        _token: str = Depends(verify_admin_role),
):
    """
    Закрыть заказ-наряд. Только для администратора.
    """
    order = await get_prefetched_order(pk, db)
    if not order:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    if not order.paid_date or order.closed_date:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='Невозможно перевести заказ в статус Закрыт')
    order.closed_date = datetime.datetime.now().date()
    db.add(order)
    await db.commit()
    return order


@order_router.post('/', response_model=OrderReadData)
async def create_order(
        order_data: OrderCreate,
        db: AsyncSession = Depends(get_db),
        _token: str = Depends(verify_admin_role),
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


class DetailUsageAddModel(pydantic.BaseModel):
    detail_id: int = pydantic.Field(ge=0)
    quantity: float = pydantic.Field(ge=0)


@order_router.post('/{pk}/details', response_model=OrderDetailData)
async def add_detail_usage(
        pk: int,
        detail_data: DetailUsageAddModel,
        db: AsyncSession = Depends(get_db),
        _token: str = Depends(verify_token),
):
    order = await db.get(models.Order, pk)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    detail = await db.get(models.Position, detail_data.detail_id)
    if not detail:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Деталь не найдена')

    if detail.is_work:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Запись должна быть деталью, а не работой.')

    detail_usage_stmt = (
        select(DetailUsage)
        .where(
            DetailUsage.position_id == detail_data.detail_id,
            DetailUsage.order_id == pk,
        )
        .limit(1)
    )
    detail_usage = (await db.execute(detail_usage_stmt)).scalars().first()
    if detail_usage:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Для этой детали уже есть запись.')

    usage = DetailUsage(
        order_id=pk,
        position_id=detail.id,
        price=detail.price,
        quantity=detail_data.quantity,
    )
    detail.in_stock_quantity -= usage.quantity  # уменьшить на использованное количество
    db.add(usage)
    db.add(detail)
    await db.commit()
    order = await get_prefetched_order(pk, db)
    return order


class DetailUsageEditModel(pydantic.BaseModel):
    price: float = pydantic.Field(ge=0)
    quantity: float = pydantic.Field(ge=0)


@order_router.put('/{order_pk}/details/{detail_pk}', response_model=OrderDetailData)
async def edit_detail_usage(
        order_pk: int,
        detail_pk: int,
        detail_data: DetailUsageEditModel,
        db: AsyncSession = Depends(get_db),
        _token: str = Depends(verify_token),
):
    """
    Изменить количеству/цену для использования запчасти.
    """
    detail = await db.get(models.Position, detail_pk)
    if not detail:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Деталь не найдена')

    usage_stmt = (
        select(DetailUsage)
        .where(DetailUsage.order_id == order_pk, DetailUsage.position_id == detail_pk)
        .limit(1)
    )
    usage = (await db.execute(usage_stmt)).scalars().first()
    if not usage:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    detail.in_stock_quantity += usage.quantity  # прибавляем то что было
    detail.in_stock_quantity -= detail_data.quantity  # забираем то, что стало

    usage.price = detail_data.price
    usage.quantity = detail_data.quantity
    db.add(usage)
    db.add(detail)
    await db.commit()
    order = await get_prefetched_order(order_pk, db)
    return order


@order_router.delete('/{order_pk}/details/{detail_pk}', response_model=OrderDetailData)
async def delete_detail_usage(
        order_pk: int,
        detail_pk: int,
        db: AsyncSession = Depends(get_db),
        _token: str = Depends(verify_token),
):
    """
    Удалить использование запчасти.
    """
    detail = await db.get(models.Position, detail_pk)
    if not detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Деталь не найдена')

    usage_stmt = (
        select(DetailUsage)
        .where(DetailUsage.order_id == order_pk, DetailUsage.position_id == detail_pk)
        .limit(1)
    )
    usage = (await db.execute(usage_stmt)).scalars().first()
    if not usage:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    detail.in_stock_quantity += usage.quantity  # прибавляем то что было

    await db.delete(usage)
    db.add(detail)
    await db.commit()
    order = await get_prefetched_order(order_pk, db)
    return order


class WorkUsageAddModel(pydantic.BaseModel):
    work_id: int = pydantic.Field(ge=0)
    quantity: float = pydantic.Field(ge=0)


@order_router.post('/{pk}/works', response_model=OrderDetailData)
async def add_work_usage(
        pk: int,
        detail_data: WorkUsageAddModel,
        db: AsyncSession = Depends(get_db),
        _token: str = Depends(verify_token),
):
    """
    Добавить к заказ-наряду новую работу.
    """
    order = await db.get(models.Order, pk)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    work = await db.get(models.Position, detail_data.work_id)
    if not work:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Работа не найдена')

    if not work.is_work:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Запись должна быть работой, а не деталью.')

    detail_usage_stmt = (
        select(WorkUsage)
        .where(
            WorkUsage.position_id == detail_data.work_id,
            WorkUsage.order_id == pk,
        )
        .limit(1)
    )
    detail_usage = (await db.execute(detail_usage_stmt)).scalars().first()
    if detail_usage:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Для этой работы уже есть запись.')

    usage = WorkUsage(
        order_id=pk,
        position_id=work.id,
        price=work.price,
        quantity=detail_data.quantity,
    )
    db.add(usage)
    await db.commit()
    order = await get_prefetched_order(pk, db)
    return order


class WorkUsageEditModel(pydantic.BaseModel):
    price: float = pydantic.Field(ge=0)
    quantity: float = pydantic.Field(ge=0)


@order_router.put('/{order_pk}/works/{work_pk}', response_model=OrderDetailData)
async def edit_work_usage(
        order_pk: int,
        work_pk: int,
        work_data: WorkUsageEditModel,
        db: AsyncSession = Depends(get_db),
        _token: str = Depends(verify_token),
):
    """
    Изменить количеству/цену для проведения работы.
    """
    work = await db.get(models.Position, work_pk)
    if not work:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Работа не найдена')

    usage_stmt = (
        select(WorkUsage)
        .where(WorkUsage.order_id == order_pk, WorkUsage.position_id == work_pk)
        .limit(1)
    )
    usage = (await db.execute(usage_stmt)).scalars().first()
    if not usage:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    usage.price = work_data.price
    usage.quantity = work_data.quantity
    db.add(usage)

    await db.commit()
    order = await get_prefetched_order(order_pk, db)
    return order


@order_router.delete('/{order_pk}/works/{detail_pk}', response_model=OrderDetailData)
async def delete_work_usage(
        order_pk: int,
        work_pk: int,
        db: AsyncSession = Depends(get_db),
        _token: str = Depends(verify_token),
):
    """
    Удалить использование работы.
    """
    work = await db.get(models.Position, work_pk)
    if not work:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Работа не найдена')

    usage_stmt = (
        select(WorkUsage)
        .where(WorkUsage.order_id == order_pk, WorkUsage.position_id == work_pk)
        .limit(1)
    )
    usage = (await db.execute(usage_stmt)).scalars().first()
    if not usage:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await db.delete(usage)

    await db.commit()
    order = await get_prefetched_order(order_pk, db)
    return order
