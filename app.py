import asyncio
import logging
from aiogram import Bot

from handlers.main_handler import *
from database.postgres_conn import create_tables, getenv


async def main():
    bot = Bot(token=getenv('TOKEN'))
    await create_tables()
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO)
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")