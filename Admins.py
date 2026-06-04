from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, FSInputFile
from aiogram.utils.formatting import Text
from aiogram.methods.send_message import SendMessage
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from Middlewares import RoleFilter, Role
from StudentDataHandler import SDH, Request
from KB import ADMIN_MAIN_MENU, RETURN_HOME, SET_TIME_MENU, fetchNotifications, buildNotificationsKeyboard, initNotificationsFile, translateWeekday, setNotification
from Config import config

import re

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
day = ""
router.message.filter(RoleFilter(Role.ADMIN, Role.OWNER))
STORAGE_DIR=config.STORAGE_FOLDER.get_secret_value()

@router.message(Command("start"))
async def greet(msg: Message):
    await msg.answer(**Text(GREETING).as_kwargs())
    await msg.answer(MAIN_MENU, reply_markup=ADMIN_MAIN_MENU)
    await initNotificationsFile()

@router.callback_query(F.data == "menus")
async def returnHome(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer()
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await bot.send_message(chat_id=callback.message.chat.id, text=MAIN_MENU, reply_markup=ADMIN_MAIN_MENU)
    await state.set_state(None)

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
async def setupNotifications(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer()

    SETUP_NOTIFICATIONS_MENU = await buildNotificationsKeyboard(callback.from_user.username)

    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text="Выберите день для настройки сообщений", reply_markup=SETUP_NOTIFICATIONS_MENU.as_markup())
    await state.set_state(None)

@router.callback_query(F.data.startswith("selected"))
async def selectDay(callback: CallbackQuery, bot: Bot, state: FSMContext):
    global day
    day = callback.data.split(" ")[1] # type: ignore
    notifications = await fetchNotifications(callback.from_user.username, day) # type: ignore
    answer_text = "Напишите время напоминания в формате *ЧЧ:ММ* для добавления/удаления напоминания\n\nВот уже установленные:\n"

    for notification in notifications:
        answer_text += (notification + "\n")

    await callback.answer()
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text=answer_text, reply_markup=SET_TIME_MENU)
    await state.set_state(SetTime.entering_time)

@router.message(StateFilter(SetTime.entering_time))
async def getTime(msg: Message):
    if re.match("\d{2}:\d{2}", msg.text): # type: ignore
        hrs, mins = msg.text.split(":")

        if int(hrs) > 23 or int(mins) > 59:
            await msg.answer("Неправильный формат: нужно _ЧЧ:ММ_", reply_markup=SET_TIME_MENU)
        else:
            global day

            await msg.answer("Вы будете уведомлены в {} каждый {}".format(msg.text, await translateWeekday(day)), reply_markup=SET_TIME_MENU)
            await setNotification(msg.from_user.username, day, msg.text)
    else:
        await msg.answer("Неправильный формат: нужно _ЧЧ:ММ_", reply_markup=SET_TIME_MENU)

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