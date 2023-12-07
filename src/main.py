import asyncio

from database.database import create_db
from view import ConsoleView
from planer import Planer
from parser import Parser
from repository import Repository


async def main():
    await create_db()
    planer = Planer(Parser(), ConsoleView(), Repository())
    await planer.start_polling()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
