from http import HTTPStatus

import jwt
from fastapi import (
    HTTPException,
    Security,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from settings import settings

security = HTTPBearer()


def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    """
    Функция для проверки JWT-токена. Декодирует токен с помощью SECRET_KEY и ALGORITHM,
    выкидывая исключения в случае ошибки.
    """
    token = credentials.credentials
    try:
        return jwt.decode(token, settings.ACCESS_TOKEN_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Token expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Invalid token')


def verify_refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    """
    Проверка refresh токена
    """
    token = credentials.credentials
    try:
        return jwt.decode(token, settings.REFRESH_TOKEN_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Refresh token expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Invalid refresh token')


def verify_mechanic_role(credentials: HTTPAuthorizationCredentials = Security(security)):
    data = verify_token(credentials)
    if data['is_mechanic'] is True:
        return data
    raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Требуется роль механика, но ее нет.')


def verify_admin_role(credentials: HTTPAuthorizationCredentials = Security(security)):
    data = verify_token(credentials)
    if data['is_admin'] is True:
        return data
    raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Требуется роль администратора, но ее нет.')
