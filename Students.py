from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.formatting import Text
from Middlewares import RoleFilter, Role

#region messages
GREETING = """
Привет! Я - бот для просмотра твоей статистики по учебным работам.
"""
#endregion

router = Router()
router.message.filter(RoleFilter(Role.STUDENT))

@router.message(CommandStart)
async def greet(msg: Message):
    await msg.answer(**Text(GREETING).as_kwargs())