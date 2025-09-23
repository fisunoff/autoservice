from http import HTTPStatus

import pydantic
from fastapi import (
    Depends,
    HTTPException, APIRouter,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import (
    Profile,
    get_db,
)
from utils.jwt_token import verify_token, verify_refresh_token
from utils.security import hash_password, verify_password, TokenFactory

auth_router = APIRouter(
    tags=['Авторизация'],
)


async def get_user(token_payload: dict = Depends(verify_token), db: AsyncSession = Depends(get_db)) -> Profile:
    user_id: int = int(token_payload.get('sub'))
    if not user_id:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='User uid not found in token')
    stmt = select(Profile).where(Profile.id == user_id, Profile.is_active == True).limit(1)
    user: Profile | None = (await db.execute(stmt)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')
    return user


class ProfileCreate(pydantic.BaseModel):
    name: str = pydantic.Field(max_length=255)
    surname: str = pydantic.Field(max_length=255)
    patronymic: str = pydantic.Field(max_length=255)
    tabel_number: str = pydantic.Field(max_length=10)
    is_admin: bool = pydantic.Field(default=False)
    is_mechanic: bool = pydantic.Field(default=False)
    login: str
    password: str


@auth_router.post('/register', status_code=HTTPStatus.CREATED)
async def register(
        user: ProfileCreate,
        db: AsyncSession = Depends(get_db)
) -> dict[str, str]:
    stmt = select(Profile).where(Profile.login == user.login).limit(1)
    existing_user: Profile | None = (await db.execute(stmt)).scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Login already registered')
    user_dict = user.model_dump()
    user_dict.pop('password')
    new_user = Profile(**user_dict, hashed_password=hash_password(user.password))
    db.add(new_user)
    await db.commit()
    return {'message': 'User created successfully'}


class UserLogin(pydantic.BaseModel):
    login: str
    password: str

@auth_router.post('/login')
async def login(
        credentials: UserLogin,
        db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    stmt = select(Profile).where(Profile.login == credentials.login).limit(1)
    user: Profile | None = (await db.execute(stmt)).scalar_one_or_none()
    if not (user and verify_password(credentials.password, user.hashed_password)):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Invalid credentials')

    access_token, refresh_token = TokenFactory().create_pair(user)

    return dict(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type='bearer',
    )

@auth_router.post('/refresh')
async def refresh(
        token_payload: dict = Depends(verify_refresh_token),
        db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    user = await get_user(token_payload=token_payload, db=db)
    access_token, refresh_token = TokenFactory().create_pair(user)
    return dict(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type='bearer',
    )
