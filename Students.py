from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.formatting import Text
from StudentDataHandler import Role, requireAcess

#region messages
greeting = """
Привет! Я - бот для просмотра твоей статистики по учебным работам.
"""
#endregion

router = Router()

@requireAcess(Role.STUDENT)
@router.message(CommandStart)
async def greet(msg: Message):
    await msg.answer(**Text(greeting).as_kwargs())

@requireAcess(Role.STUDENT)
async def showInfo(msg: Message):
    await msg.answer("ashdalksjsldf") # change later to DB fetch