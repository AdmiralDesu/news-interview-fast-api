from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy.future import select
from models.news_models import News
from datetime import date


async def get_news_from_db(
        start_date: date,
        end_date: date,
        session: AsyncSession
) -> List[News]:

    result = await session.execute(
        select(News).filter(
            News.news_date.between(
                start_date,
                end_date
            )
        )
    )

    news: List[News] = result.scalars().all()

    return news

