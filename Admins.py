from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, FSInputFile
from aiogram.utils.formatting import Text
from aiogram.methods.send_message import SendMessage
from aiogram import F
from Middlewares import RoleFilter, Role
from StudentDataHandler import SDH, Request
from KB import ADMIN_MAIN_MENU
from Config import config

import json

# region messages
GREETING = """
Здравствуйте! Я - бот для помощи студентам в отслеживании их прогресса по работам.

Используйте меня для администрирования информации, которую видят слушатели.
"""
MAIN_MENU = """
*ГЛАВНОЕ МЕНЮ*

Здесь у Вас есть доступ ко всем функциям бота, включая проверку данных слушателей (_как у самих слушателей_).
"""
SEND_ROLES_HINT = """
*Отправьте сводную таблицу с ролями*

_Структура содержания_
2 столбца. Первая строка - шапка. В ней писать можно всё, что угодно.
Далее в левом столбце вставьте fullname или кодовое слово admin (case-sensitive),
в правый же столбец вставьте юзернеймы, соответствующие fullname.
"""
SEND_INFO_HINT = """
*Отправьте таблицу с результатами слушателей*

_Структура содержания_
В таблице предусмотрено 25 столбцов (Студент, Презентация (PPTX), ..., Руководитель, Консультант).
Первая строка, как обычно, шапка.

⚠️‼️*_ОБРАТИТЕ ВНИМАНИЕ НА ФОРМАТ ИМЕНИ_*‼️
"kidp\_stats\_one\_excel\_ГГГГ-ММ-ДД.xlsx"
_Пока программа не предусматривает "умный" парсинг имени._
_В случае ошибки, файл не будет принят._
"""
# endregion
router = Router()
router.message.filter(RoleFilter(Role.ADMIN, Role.OWNER))
STORAGE_DIR=config.STORAGE_FOLDER.get_secret_value()
notifications = []

@router.message(CommandStart)
async def greet(msg: Message):
    await msg.answer(**Text(GREETING).as_kwargs())
    await msg.answer(MAIN_MENU, reply_markup=ADMIN_MAIN_MENU)

@router.callback_query(F.data.startswith("update"))
async def getUpdatedData(callback: CallbackQuery, bot: Bot):
    function = callback.data.split(" ")[1] # type: ignore

    if function == "users":
        await callback.answer()

        hint_pic = InputMediaPhoto(media=FSInputFile("message_media/users_table_struct.jpeg"), caption=SEND_ROLES_HINT)

        await bot.edit_message_media(chat_id=callback.message.chat.id, message_id=callback.message.message_id, media=hint_pic) # type: ignore
        pass
    elif function == "DB":
        await callback.answer()
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text=SEND_INFO_HINT) # type: ignore
        pass

async def fetchNotifications(username: str) -> dict:
    with open(STORAGE_DIR + "notifications.json", "r", encoding="utf-8") as F:
        total = json.load(F)

@router.callback_query(F.data == "notifications setup")
async def setupNotifications(callback: CallbackQuery):
    pass

"""{
    "users": [
        {
            "username": "@<username>",
            "times": [
                {"monday": "10:35"},
                {"monday": "11:15"},
                {"tuesday": "14:18"}
            ],
        },
        {
            "username": "@<another_usrname>",
            "times": [
                {"friday": "23:59"},
                {"saturday": "12:14"},
                {"saturday": "8:45"},
                {"saturday": "6:54"}
            ]
        }
    ]
}"""