import KB

#region Messages
greeting = """
Привет, {}! Используй меня для отслеживания своих результатов по работам!
"""
#endregion

from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.formatting import Text
import StudentDataHandler as SDH

router = Router()

@router.message(CommandStart())
async def startHandler(msg: Message):
    await msg.answer(**Text(greeting.format(msg.from_user.username)).as_kwargs()) # type: ignore