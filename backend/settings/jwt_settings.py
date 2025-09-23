import os

__all__ = [
    'JWTSettings',
]

from datetime import timedelta


class JWTSettings:
    @property
    def ACCESS_TOKEN_SECRET_KEY(self) -> str:
        return os.getenv('ACCESS_TOKEN_SECRET_KEY')

    @property
    def REFRESH_TOKEN_SECRET_KEY(self) -> str:
        return os.getenv('REFRESH_TOKEN_SECRET_KEY')

    @property
    def JWT_ALGORITHM(self) -> str:
        return os.getenv('JWT_ALGORITHM')

    @property
    def ACCESS_TOKEN_EXPIRE_MINUTES(self) -> timedelta:
        return timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 60)))

    @property
    def REFRESH_TOKEN_EXPIRE_MINUTES(self) -> timedelta:
        return timedelta(minutes=int(os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES', 60*60*30)))
