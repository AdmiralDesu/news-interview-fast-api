from __future__ import annotations
from collections import namedtuple
from typing import NamedTuple
from bs4 import BeautifulSoup
import requests


class MosDay:
    def __init__(self):
        self.BASE_URL = 'http://mosday.ru/'
        self.news = namedtuple('News', ['id', 'cover', 'title', 'publish_date', 'description'])
        self.news_table: list = self.get_bs_tags

        self.bs = None
        self.note_idx = None
        self.table_idx = None

    @property
    def get_html(self) -> str:
        r = requests.get(self.BASE_URL + 'news/tags.php?metro')
        return r.text

    @property
    def get_bs_tags(self) -> list:
        bs = BeautifulSoup(self.get_html, 'html.parser')
        return bs.findAll('table')[8:10]

    @property
    def get_publish_date(self):
        return self.news_table[0].find('b').text

    @property
    def extract_idx(self) -> int:
        return self.bs[self.note_idx].findAll('a')[0]['href'].split('&')[0].split('?')[1]

    @property
    def extract_cover(self) -> str | None:
        try:
            cover = self.bs[self.note_idx].img['src']
        except TypeError:
            cover = None

        return cover

    @property
    def extract_title(self) -> str:
        return self.bs[self.note_idx].findAll('b')[1].text

    @property
    def extract_description(self) -> str:
        return self.bs[self.note_idx].i.text

    @property
    def get_news_info(self) -> NamedTuple:
        return self.news(self.extract_idx, self.extract_cover, self.extract_title, self.get_publish_date,
                         self.extract_description)

    def get_all_news(self) -> list:
        all_news = list()
        for self.table_idx in range(2):
            self.bs = self.news_table[self.table_idx].findAll('tr')
            for self.note_idx in range(25):
                all_news.append(self.get_news_info)

        return all_news


if __name__ == '__main__':
    print(MosDay().get_all_news())
