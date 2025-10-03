from fastapi import APIRouter, Depends, HTTPException
from jwt_token import verify_admin_token
from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from models import get_db, Position
from schemas.pricelist import PositionData, BasePositionData
from utils.jwt_token import verify_token

price_list_router = APIRouter(
    tags=['Прейскурант'],
)


@price_list_router.get('/', response_model=list[PositionData])
async def get_price_list(
    db: AsyncSession = Depends(get_db),
    _token_payload: dict = Depends(verify_token),
) -> Sequence[PositionData]:
    """
    Весь прейскурант
    """
    stmt = select(Position)
    results = (await db.execute(stmt)).scalars().all()
    return results

@price_list_router.get('/details', response_model=list[PositionData])
async def get_details(
    db: AsyncSession = Depends(get_db),
    _token_payload: dict = Depends(verify_token),
) -> Sequence[PositionData]:
    """
    Получить все запчасти.
    """
    stmt = select(Position).where(Position.is_work == False)
    results = (await db.execute(stmt)).scalars().all()
    return results

@price_list_router.get('works', response_model=list[PositionData])
async def get_works(
    db: AsyncSession = Depends(get_db),
    _token_payload: dict = Depends(verify_token),
) -> Sequence[PositionData]:
    """
    Получить все работы.
    """
    stmt = select(Position).where(Position.is_work == True)
    results = (await db.execute(stmt)).scalars().all()
    return results

@price_list_router.post('/', response_model=PositionData)
async def create_position(
        data: BasePositionData,
        db: AsyncSession = Depends(get_db),
        _admin_token: dict = Depends(verify_admin_token),
):
    """
    Добавить позицию в прайс-лист. Только для администратора.
    """
    position = Position(**data.model_dump())
    db.add(position)
    await db.commit()
    await db.refresh(position)
    return position

@price_list_router.put('/{_id}', response_model=PositionData)
async def update_position(
        _id: int,
        data: BasePositionData,
        db: AsyncSession = Depends(get_db),
        _admin_token: dict = Depends(verify_admin_token),
) -> PositionData:
    """
    Изменить позицию в прайс-листе. Только для администратора.
    """
    stmt = select(Position).where(Position.id == _id).limit(1)
    result = (await db.execute(stmt)).scalars().first()
    if not result:
        raise HTTPException(status_code=404, detail='Позиция прейскуранта не найдена')
    result = Position(**data.model_dump())
    db.add(result)
    await db.commit()
    await db.refresh(result)
    return result

@price_list_router.delete('/{_id}', response_model=PositionData)
async def delete_position(
        _id: int,
        db: AsyncSession = Depends(get_db),
        _admin_token: dict = Depends(verify_admin_token),
):
    """
    Сделать позицию неактивной
    """
    stmt = select(Position).where(Position.id == _id).limit(1)
    result = (await db.execute(stmt)).scalars().first()
    if not result:
        raise HTTPException(status_code=404, detail='Позиция прейскуранта не найдена')
    result.using = False
    db.add(result)
    await db.commit()
    await db.refresh(result)
    return result
