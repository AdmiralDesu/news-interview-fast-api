import aiosqlite
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.news_models import News
from datetime import date
from typing import NamedTuple, List
import sqlite3
from sqlalchemy import func


async def get_news_from_db(
        start_date: date,
        end_date: date,
        session: AsyncSession
) -> List[News]:
    print(f'{start_date=}\n{end_date=}')

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


async def add_news_to_db(
        news_tuple: List[NamedTuple]
):
    async with aiosqlite.connect('./database.db') as session:

        for headline in news_tuple:
            try:
                await session.execute(
                    f"""
                    INSERT INTO news 
                    (news_id, title, news_image, news_date)
                    VALUES 
                    (
                        "{headline.id}", 
                        "{headline.title.replace('"', "'")}", 
                        "{headline.cover}", 
                        "{headline.publish_date}"
                    )
                    """
                )
                print(f'Работаю над новостью {headline.id=}')

                await session.commit()
                print(f'Новость с {headline.id=} создана')
            except sqlite3.IntegrityError:
                pass
