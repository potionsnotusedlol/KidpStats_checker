from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.formatting import Text
from aiogram import F
from Middlewares import RoleFilter, Role

from KB import admin_main_menu

# region messages
GREETING = """
Здравствуйте! Я - бот для помощи студентам в отслеживании их прогресса по работам.

Используйте меня для администрирования информации, которую видят слушатели.
"""
MAIN_MENU = """
*ГЛАВНОЕ МЕНЮ*

Здесь у Вас есть доступ ко всем функциям бота, включая проверку данных слушателей (_как у самих слушателей_).
"""
# endregion
router = Router()
router.message.filter(RoleFilter(Role.ADMIN, Role.OWNER))

@router.message(CommandStart)
async def greet(msg: Message):
    await msg.answer(**Text(GREETING).as_kwargs())
    await msg.answer(MAIN_MENU, reply_markup=admin_main_menu.as_markup())

@router.callback_query(F.data.startswith("update"))
async def getUpdatedData(callback: CallbackQuery):
    function = callback.data.split(" ")[1] # type: ignore

    if function == "users":
        pass
    elif function == "DB":
        pass