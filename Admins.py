from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.formatting import Text
from StudentDataHandler import Role, requireAcess, getUserRole

import KB

# region messages
greeting = """
Здравствуйте! Я - бот для помощи студентам в отслеживании их прогресса по работам.

Используйте меня для администрирования информации, которую видят слушатели.
"""
main_menu = """
ГЛАВНОЕ МЕНЮ

Здесь у Вас есть доступ ко всем функциям бота, включая проверку данных слушателей (_как у самих слушателей_).
"""
# endregion
router = Router()
role = 0

@requireAcess(Role.ADMIN)
@router.message(Command("start"))
async def greet(msg: Message):
    await msg.answer(**Text(greeting).as_kwargs())

    await msg.answer(main_menu, reply_markup=KB.admin_main_menu)