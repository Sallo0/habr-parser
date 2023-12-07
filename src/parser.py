from datetime import datetime

from bs4 import BeautifulSoup

from entities import ArticleInfo


class Parser:

    def __init__(self):
        pass

    def get_articles_urls(self, hub_page: str) -> list[str]:
        parser = BeautifulSoup(hub_page, features='lxml')
        articles_urls = parser.find_all('a', class_='tm-title__link')
        articles_urls = ["https://habr.com" + article_url.get('href') for article_url in articles_urls]
        return articles_urls

    def parse_article(self, article_page: str) -> ArticleInfo:
        parser = BeautifulSoup(article_page, features='lxml')

        title = parser.find('div', class_='tm-article-presenter__header').find('h1', class_='tm-title').text

        author = parser.find('a', class_='tm-user-info__username')

        author_name = author.text.strip()

        text = parser.find('div', class_='article-formatted-body').text

        author_url = "https://habr.com" + author.get('href')

        pub_date = parser.find('span', class_='tm-article-datetime-published').find('time').get('datetime')

        pub_date = datetime.strptime(pub_date, '%Y-%m-%dT%H:%M:%S.%fZ')

        return ArticleInfo(title=title, pub_date=pub_date, author_url=author_url, author_username=author_name,
                           text=text)
