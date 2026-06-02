from aiogram import Router, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, FSInputFile
from aiogram.utils.formatting import Text
from aiogram.methods.send_message import SendMessage
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from Middlewares import RoleFilter, Role
from StudentDataHandler import SDH, Request
from KB import ADMIN_MAIN_MENU, RETURN_HOME, fetchNotifications, buildNotificationsKeyboard, initNotificationsFile
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

@router.message(CommandStart)
async def greet(msg: Message):
    await msg.answer(**Text(GREETING).as_kwargs())
    await msg.answer(MAIN_MENU, reply_markup=ADMIN_MAIN_MENU)
    await initNotificationsFile()

@router.callback_query(F.data == "menus")
async def returnHome(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await bot.send_message(chat_id=callback.message.chat.id, text=MAIN_MENU, reply_markup=ADMIN_MAIN_MENU)

@router.callback_query(F.data.startswith("update"))
async def getUpdatedData(callback: CallbackQuery, bot: Bot):
    function = callback.data.split(" ")[1] # type: ignore

    if function == "users":
        await callback.answer(reply_markup=RETURN_HOME)

        hint_pic = InputMediaPhoto(media=FSInputFile("message_media/users_table_struct.jpeg"))

        await bot.edit_message_media(chat_id=callback.message.chat.id, message_id=callback.message.message_id, media=hint_pic, reply_markup=RETURN_HOME) # type: ignore
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text=SEND_ROLES_HINT)
        pass
    elif function == "DB":
        await callback.answer()
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text=SEND_INFO_HINT, reply_markup=RETURN_HOME) # type: ignore
        pass

class SetTime(StatesGroup):
    entering_time = State()

@router.callback_query(F.data == "notifications setup")
async def setupNotifications(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    SETUP_NOTIFICATIONS_MENU = await buildNotificationsKeyboard(callback.from_user.username)
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text="Выберите день для настройки сообщений", reply_markup=SETUP_NOTIFICATIONS_MENU.as_markup())

@router.callback_query(F.data.startswith("selected"))
async def selectDay(callback: CallbackQuery):
    day = callback.data.split(" ")[1] # type: ignore
    notifications = await fetchNotifications(callback.from_user.username, day) # type: ignore
    answer_text = "Напишите время напоминания в формате *ЧЧ:ММ* для добавления/удаления напоминания\n"

    for notification in notifications:
        answer_text += (notification + "\n")

    callback.answer(answer_text, reply_markup=RETURN_HOME)


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