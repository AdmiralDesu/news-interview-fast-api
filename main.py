from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from services.services import get_news_from_db
from models.news_models import News
from datetime import date
from typing import List
from fastapi_utils.tasks import repeat_every
from mosday import MosDay

app = FastAPI()
parser = MosDay()


@app.get('/{date_from}-{date_to}')
async def get_news_by_date(
        date_from: str,
        date_to: str,
        session: AsyncSession = Depends(get_session)
) -> List[News]:

    """

    :param date_from: Начальная дата
    :param date_to: Конечная дата
    :param session: Сессия к базе
    :return: Список всех новостей за определенную дату
    """

    try:
        list_of_start_dates = [
            int(x) for x in date_from.split('.')
        ]

        start_date = date(
            year=list_of_start_dates[0],
            month=list_of_start_dates[1],
            day=list_of_start_dates[2]
        )

        list_of_end_dates = [
            int(x) for x in date_to.split('.')
        ]

        end_date = date(
            year=list_of_end_dates[0],
            month=list_of_end_dates[1],
            day=list_of_end_dates[2]
        )
    except IndexError:
        raise HTTPException(
            status_code=500,
            detail='Даты указаны неверно'
        )

    news: List[News] = await get_news_from_db(
        start_date=start_date,
        end_date=end_date,
        session=session
    )

    if news:
        return news
    else:
        raise HTTPException(
            status_code=404,
            detail='Новостей за данный период нет'
        )


@app.get('/')
async def redirect():
    return RedirectResponse('/docs')


@app.on_event('startup')
@repeat_every(seconds=30, wait_first=False, raise_exceptions=True)
async def update_base() -> None:
    news_tuple = parser.get_all_news()
    print(f'{news_tuple=}')
    session = await get_session().__anext__()
    for headline in news_tuple:
        new_news = News(
            news_id=headline.id,
            news_image=headline.cover,
            news_title=headline.title,
            news_date=headline.publish_date
        )
        session.add(new_news)

        print(f'Новость с {headline.id=} создана')
        await session.commit()
        await session.refresh(new_news)
    print('Добавление окончено')

