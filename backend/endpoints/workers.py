from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

import endpoints.auth
from models import get_db, Profile
from schemas.worker import ReadWorkerData, ProfileCreate
from utils.jwt_token import verify_admin_role

workers_router = APIRouter(
    tags=['Сотрудники'],
)


@workers_router.get('/', response_model=list[ReadWorkerData])
async def get_workers(
        db: AsyncSession = Depends(get_db),
        _token_payload: dict = Depends(verify_admin_role),
) -> Sequence[ReadWorkerData]:
    """
    Список всех сотрудников (в том числе и уже уволенных).
    Доступно только администратору.
    """
    stmt = select(Profile)
    results = (await db.execute(stmt)).scalars().all()
    return results


@workers_router.post('/hire', response_model=ReadWorkerData)
async def hire(
        user: ProfileCreate,
        db: AsyncSession = Depends(get_db),
        _token_payload: dict = Depends(verify_admin_role),
):
    """
    Нанять сотрудника на работу. Доступно администратору.
    """
    return endpoints.auth.register(user, db=db)


@workers_router.post('/{pk}/fire', response_model=ReadWorkerData)
async def fire(
        pk: int,
        db: AsyncSession = Depends(get_db),
        _token_payload: dict = Depends(verify_admin_role),
):
    """
    Уволить сотрудника. Доступно администратору.
    """
    stmt = select(Profile).where(Profile.id == pk)
    worker = (await db.execute(stmt)).scalars().first()
    if not worker:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,)
    worker.is_active = False
    await db.commit()
    return worker
