import KB

#region Messages
greeting = """
Бот в разработке, больше не приходи)
"""
#endregion

from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.utils.formatting import Text

router = Router()

@router.message(CommandStart())
async def startHandler(msg: Message):
    await msg.answer(**Text(greeting).as_kwargs()) # type: ignore