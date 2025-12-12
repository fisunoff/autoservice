from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import date, timedelta
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from models import get_db, Position, DetailUsage, Order
from schemas.leftovers import LeftOverData
from utils.jwt_token import verify_token

leftovers_router = APIRouter(
    tags=['Складские остатки'],
)

@leftovers_router.get('/', response_model=list[LeftOverData])
async def get_leftovers(
    db: AsyncSession = Depends(get_db),
    _token_payload: dict = Depends(verify_token),
):
    stmt = select(Position).where(Position.is_work == False)
    leftovers = (await db.execute(stmt)).scalars().all()

    max_age = 30
    cutoff_date = date.today() - timedelta(days=max_age)
    stmt = (
        select(DetailUsage)
        .join(DetailUsage.order)  # INNER JOIN orders
        .where(Order.opened_date >= cutoff_date)  # условие по дате
        .options(joinedload(DetailUsage.order))  # опционально: подгрузить Order
    )
    usages = (await db.execute(stmt)).scalars().all()

    result_map: dict[int, LeftOverData] = {
        row.id : LeftOverData(
            id=row.id,
            title=row.title,
            unit=row.unit,
            price=row.price,
            in_stock_quantity=row.in_stock_quantity,
            using=row.using,
            last_month_usage=0.0,
        )
        for row in leftovers
    }

    for usage in usages:
        result_map[usage.order.id].last_month_usage += usage.quantity

    return list(result_map.values())
