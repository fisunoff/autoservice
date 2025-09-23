from datetime import (
    datetime,
    timedelta,
)
from http import HTTPStatus

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from pydantic import BaseModel

from models import Profile
from settings import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

__all__ = [
    'hash_password',
    'verify_password',
    'TokenFactory',
]


class TokenPayload(BaseModel):
    sub: str
    is_admin: bool
    is_mechanic: bool


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


class TokenFactory:
    def _get_token_payload(self, user: Profile) -> TokenPayload:
        if not user.is_active:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Inactive user')
        return TokenPayload(
            sub=str(user.id),
            is_admin=user.is_admin,
            is_mechanic=user.is_mechanic,
        )

    def _create_token(self, token_payload: TokenPayload, expires_delta: timedelta, secret_key: str) -> str:
        to_encode = token_payload.model_dump()
        expire = datetime.now() + expires_delta
        to_encode.update({'exp': expire})
        return jwt.encode(to_encode, secret_key, algorithm=settings.JWT_ALGORITHM)

    def create_access_token(self, user: Profile) -> str:
        return self._create_token(
            token_payload=self._get_token_payload(user),
            expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            secret_key=settings.ACCESS_TOKEN_SECRET_KEY,
        )

    def create_refresh_token(self, user: Profile):
        return self._create_token(
            token_payload=self._get_token_payload(user),
            expires_delta=settings.REFRESH_TOKEN_EXPIRE_MINUTES,
            secret_key=settings.REFRESH_TOKEN_SECRET_KEY,
        )

    def create_pair(self, user: Profile) -> tuple[str, str]:
        return self.create_access_token(user), self.create_refresh_token(user)
