from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Customer, get_db
from schemas.customer import CustomerData, BaseCustomerData
from utils.jwt_token import verify_token

customer_router = APIRouter(
    tags=['Клиент'],
)

@customer_router.get('/', response_model=list[CustomerData])
async def get_clients(
        db: AsyncSession = Depends(get_db),
        _token_payload: dict = Depends(verify_token),
) -> list[CustomerData]:
    """
    Список всех клиентов.
    """
    stmt = select(Customer)
    results = (await db.execute(stmt)).scalars().all()
    return results

@customer_router.post('/', response_model=CustomerData)
async def create_customer(
        data: BaseCustomerData,
        db: AsyncSession = Depends(get_db),
        _token_payload: dict = Depends(verify_token),
):
    """
    Добавить клиента.
    """
    customer = Customer(**data.model_dump())
    db.add(customer)
    await db.commit()
    await db.refresh(customer)
    return customer

# todo: детальный просмотр со связанным заказ-нарядами
