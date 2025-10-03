from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY

import models

__all__ = [
    'Article',
]


class Article(models.Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    brands = Column(ARRAY(String), nullable=False)
    syndrome = Column(Text)
    solution = Column(Text)
