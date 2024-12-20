import asyncio
import logging
import sys
from config import API_TOKEN
from commands import router as main_router

from aiogram import Dispatcher, Bot

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot)

dp.include_router(main_router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())