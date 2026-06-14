import asyncio
import logging
import admins.admins as Admins
import students
import guests

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client import default
from config import config
from middlewares import InitMiddleware
from datahdl import get_user_db, autofetch_dir
from admins.notifications import run_scheduler

pm_options = { ParseMode.MARKDOWN_V2: "MARKDOWN_V2" }

async def main():
    bot = Bot(token=config.BOT_TOKEN.get_secret_value(), default=default.DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    dp = Dispatcher(storage=MemoryStorage())
    dp.update.outer_middleware(InitMiddleware())
    dp.callback_query.middleware(InitMiddleware())
    dp.include_routers(Admins.router, students.router, guests.router)

    asyncio.create_task(run_scheduler(bot))
    await get_user_db()
    await autofetch_dir(config.STORAGE_FOLDER.get_secret_value())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())