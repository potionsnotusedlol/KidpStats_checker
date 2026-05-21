import asyncio
import logging
import Admins
import Students
import Guests

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client import default
from Config import config
from Middlewares import InitMiddleware
from StudentDataHandler import getUsersDB

pm_options = { ParseMode.MARKDOWN_V2: "MARKDOWN_V2" }

async def main():
    bot = Bot(token=config.BOT_TOKEN.get_secret_value(), default=default.DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    dp = Dispatcher(storage=MemoryStorage())
    dp.update.outer_middleware(InitMiddleware())
    dp.callback_query.middleware(InitMiddleware())
    dp.include_routers(Admins.router, Students.router, Guests.router)

    await getUsersDB()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())