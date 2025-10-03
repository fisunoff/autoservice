import pydantic
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from models import get_db, Article
from schemas.wiki import WikiData, WikiBaseData
from utils.jwt_token import verify_token, verify_mechanic_role

wiki_router = APIRouter(
    tags=['База знаний'],
)


class WikiOptionsResponse(pydantic.BaseModel):
    options: dict[str, list[str]]


@wiki_router.options('/')
async def get_options(
        db: AsyncSession = Depends(get_db),
        _token: str = Depends(verify_token),
):
    """
    Все варианты брендов, которые уже есть.
    """
    stmt = (
        select(func.unnest(Article.brands).label('brands'))
        .distinct()
        .order_by(text('brands'))
    )
    result = (await db.execute(stmt)).scalars().all()
    return WikiOptionsResponse(
        options={
            'brands': list(result),
        }
    )


@wiki_router.get('/', response_model=list[WikiData])
async def get_wiki(
        db: AsyncSession = Depends(get_db),
        _token: str = Depends(verify_token),
):
    """
    Получить все статьи.
    """
    stmt = select(Article)
    results = (await db.execute(stmt)).scalars().all()
    return results


@wiki_router.post('/', response_model=WikiData, status_code=status.HTTP_201_CREATED)
async def create_wiki(
        data: WikiBaseData,
        db: AsyncSession = Depends(get_db),
        _token: str = Depends(verify_mechanic_role),
) -> WikiData:
    article = Article(**data.model_dump())
    db.add(article)
    await db.commit()
    await db.refresh(article)
    return article


@wiki_router.put('/{pk}', response_model=WikiData)
async def update_wiki(
        pk: int,
        data: WikiBaseData,
        db: AsyncSession = Depends(get_db),
        _token: str = Depends(verify_mechanic_role),
) -> WikiData:
    """
    Обновить статью. Доступно механику.
    """
    stmt = select(Article).where(Article.id == pk).limit(1)
    result = (await db.execute(stmt)).scalars().first()
    if not result:
        raise HTTPException(status_code=404, detail='Статья не найдена')
    result = Article(**data.model_dump())
    db.add(result)
    await db.commit()
    await db.refresh(result)
    return result


@wiki_router.delete('/{pk}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_wiki(
        pk: int,
        db: AsyncSession = Depends(get_db),
        _token: str = Depends(verify_mechanic_role),
):
    stmt = select(Article).where(Article.id == pk).limit(1)
    result = (await db.execute(stmt)).scalars().first()
    if not result:
        raise HTTPException(status_code=404, detail='Статья не найдена')
    await db.delete(result)
    await db.commit()
