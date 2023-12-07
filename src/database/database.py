from sqlalchemy import insert, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from database.models import Base

from config import settings

DB_URL = settings.DB_URL

engine = create_async_engine(DB_URL,
                             # echo=True,
                             )

async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)

        # test data
        await conn.execute(text(
            "insert into hub values ('Программирование', 'https://habr.com/ru/hubs/programming/articles/',1, '2021-10-10 00:00:00'),"
                                "('Учебный процесс в IT', 'https://habr.com/ru/hubs/study/articles/',1, '2021-10-10 00:00:00')"
            "on conflict do nothing;")
        )
