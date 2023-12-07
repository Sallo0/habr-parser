from asyncpg import UniqueViolationError
from sqlalchemy import func, select, insert, update
from sqlalchemy.exc import IntegrityError

from database.database import async_session_maker
from database.models import Author, Article, Hub
from entities import ArticleInfo, HubInfo
from datetime import datetime


class Repository:
    async def create_or_get_author(self, article_data: ArticleInfo) -> Author | None:

        if not article_data.author_username:
            return None

        async with async_session_maker() as session:
            async with session.begin():
                try:
                    await session.execute(
                        insert(Author).values(username=article_data.author_username, url=article_data.author_url)
                    )
                except IntegrityError:
                    pass

            author = await session.execute(
                select(Author).where(Author.__table__.c.username == article_data.author_username)
            )
            author = author.scalar_one_or_none()
        return author

    async def save_article(self, article_data: ArticleInfo) -> None:
        async with async_session_maker() as session:
            existing_author = await self.create_or_get_author(article_data)

            hub = await session.scalar(
                select(Hub).where(Hub.url == article_data.hub_url)
            )

            article = await session.scalar(
                select(Article).where(Article.url == article_data.article_url)
            )

            if not article:
                article = Article(
                    title=article_data.title,
                    url=article_data.article_url,
                    text=article_data.text,
                    pub_date=article_data.pub_date,
                    author_id=existing_author.id if existing_author else None)
                article.hubs.append(hub)

            elif hub not in await article.awaitable_attrs.hubs:
                (await article.awaitable_attrs.hubs).append(hub)

            session.add(article)
            await session.commit()

    async def get_hubs_to_parse(self) -> list[HubInfo]:
        async with async_session_maker() as session:
            current_date = datetime.now()

            time_diff = func.extract('epoch', current_date - Hub.__table__.c.last_update)

            query = select(Hub.__table__.c.id, Hub.__table__.c.url).where(
                time_diff >= Hub.__table__.c.update_information_period * 60)

            hubs_to_update = await session.execute(query)

            hubs = []
            for hub in hubs_to_update:
                updated_hub = await session.execute(
                    update(Hub).where(Hub.__table__.c.id == hub.id).values(last_update=datetime.now()).returning(
                        Hub.__table__.c.name, Hub.__table__.c.url))
                hubs.append(HubInfo(**updated_hub.mappings().first()))
            await session.commit()

        return hubs
