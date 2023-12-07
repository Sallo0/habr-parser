import datetime

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class Author(Base):
    __tablename__ = 'author'

    url: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)

    articles: Mapped[list["Article"]] = relationship(back_populates="author", uselist=True)

    __table_args__ = (
        UniqueConstraint('url', name='unique_author_username'),
    )


class Hub(Base):
    __tablename__ = 'hub'

    name: Mapped[str] = mapped_column(unique=True)
    url: Mapped[str] = mapped_column(unique=True)
    update_information_period: Mapped[int] = mapped_column()
    last_update: Mapped[datetime.datetime] = mapped_column()

    articles: Mapped[list["Article"]] = relationship(secondary='article_hub_association', back_populates='hubs',
                                                     uselist=True)

    __table_args__ = (
        UniqueConstraint('url', name='unique_hub_url'),
    )


class Article(Base):
    __tablename__ = 'article'

    title: Mapped[str] = mapped_column()
    url: Mapped[str] = mapped_column(unique=True)
    text: Mapped[str] = mapped_column(nullable=True)
    pub_date: Mapped[datetime.datetime] = mapped_column()

    author_id: Mapped[int] = mapped_column(ForeignKey('author.id'))
    author: Mapped[Author] = relationship(back_populates="articles", uselist=False)

    hubs: Mapped[list[Hub]] = relationship(secondary='article_hub_association', back_populates='articles', uselist=True)

    __table_args__ = (
        UniqueConstraint('url', name='unique_article_url'),
    )


class ArticleHubAssociation(Base):
    __tablename__ = 'article_hub_association'

    article_id: Mapped[int] = mapped_column(ForeignKey('article.id'))
    hub_id: Mapped[int] = mapped_column(ForeignKey('hub.id'))
