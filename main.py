import os
from dotenv import load_dotenv
import asyncio
import logging
from aiogram import Bot, Dispatcher

from app.handlers import router
from app.database.model import async_main

async def main():

    await async_main()

    load_dotenv()

    bot = Bot(token = os.getenv('BOT_TOKEN'))
    dp = Dispatcher()

    dp.include_routers(router)
    await dp.start_polling(bot)

    print("Bot started")

if __name__ == "__main__":

    #logging.basicConfig(level = logging.INFO)
    
    try: 
        asyncio.run(main())

    except KeyboardInterrupt:
        print("Exit")