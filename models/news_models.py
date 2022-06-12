from sqlmodel import SQLModel, Field


class NewsBase(SQLModel):
    title: str = Field(nullable=False, index=True)
    news_image: str = Field(nullable=False, index=True)
    news_date: str = Field(nullable=False, index=True)


class News(NewsBase, table=True):
    news_id: int = Field(nullable=False, primary_key=True)


class NewsCreate(NewsBase):
    news_id: int
