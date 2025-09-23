import os

__all__ = [
    'DatabaseSettings',
]


class DatabaseSettings:
    @property
    def DATABASE_URL(self) -> str:
        return os.getenv('DATABASE_URL')
