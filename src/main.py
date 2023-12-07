import asyncio
from parser import Parser

from database.database import create_db
from manager import Manager
from repository import Repository
from view import ConsoleView


async def main():
    await create_db()
    planer = Manager(Parser(), ConsoleView(), Repository())
    await planer.start_polling()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
