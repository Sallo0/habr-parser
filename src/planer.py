import asyncio
import logging
import time
import traceback

import aiohttp
from aiohttp import ClientSession

from parser import Parser
from entities import ArticleInfo, HubInfo
from view import ConsoleView
from repository import Repository


class Planer:
    def __init__(self, parser: Parser, view: ConsoleView, repository: Repository):
        self.parser = parser
        self.view = view
        self.repository = repository

    async def start_polling(self) -> None:
        try:
            while True:
                time.sleep(1)
                hubs_to_parse = await self.repository.get_hubs_to_parse()
                if not hubs_to_parse:
                    continue

                try:
                    async with aiohttp.ClientSession() as session:
                        for hub_data in hubs_to_parse:
                            hub_url = hub_data.url
                            hub_page = await self.get_hub(session, hub_url)
                            articles_urls = self.parser.get_articles_urls(hub_page)

                            tasks = [asyncio.create_task(self.process_article(session, article_url, hub_data)) for
                                     article_url in articles_urls]
                            self.view.display_hub(hub_data)
                            for article_task in asyncio.as_completed(tasks):
                                article = await article_task
                                self.view.display_article(article)

                except aiohttp.ClientConnectorError:
                    print("Сайт недоступен, пробую подлючиться повторно")

        except Exception as e:
            traceback.print_exc()

        finally:
            print("Завершение работы")

    async def get_hub(self, session: ClientSession, hub_url: str) -> str:
        async with session.get(hub_url) as response:
            return await response.text()

    async def process_article(self, session: ClientSession, article_url: str, hub_info: HubInfo) -> ArticleInfo | None:
        async with session.get(article_url) as response:
            article = await response.text()

            try:
                article_info = self.parser.parse_article(article)
            except AttributeError as e:
                logging.error(f"Ошибка при парсинге статьи {article_url}")
                # logging.error(traceback.format_exc())
                return

            article_info.article_url = article_url
            article_info.hub_url = hub_info.url
            await self.repository.save_article(article_info)
            return article_info
