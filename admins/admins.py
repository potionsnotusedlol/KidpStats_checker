from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, FSInputFile
from aiogram.utils.formatting import Text
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from middlewares import RoleFilter, Role
from keyboards import (
    ADMIN_MAIN_MENU,
    RETURN_HOME,
    SET_TIME_MENU,
    build_notifications_keyboard
)
from admins.notifications import (
    init_notifications_file,
    fetch_notifications,
    translate_weekday,
    set_notification,
    remove_notification
)
from datahdl import SDH, Request
from config import config

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

⚠️‼️*ОБРАТИТЕ ВНИМАНИЕ НА ФОРМАТ ИМЕНИ*‼️
"kidp\_stats\_one\_excel\_ГГГГ-ММ-ДД.xlsx"
_Пока программа не предусматривает "умный" парсинг имени._
_В случае ошибки, файл не будет принят._
"""
# endregion
router = Router()
day = ""
router.message.filter(RoleFilter(Role.ADMIN, Role.OWNER))

@router.message(Command("start"))
async def greet(msg: Message) -> None:
    """
    Sends greeting message for admin-level (and above) users.

    :param msg: :class:`Message` instance for a handler
    :return: Returns :type:`None`, just answers the _/start_ message
    """

    await msg.answer(**Text(GREETING).as_kwargs())
    await msg.answer(MAIN_MENU, reply_markup=ADMIN_MAIN_MENU)
    await init_notifications_file()

@router.callback_query(F.data == "menus")
async def return_home(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """
    Switches bot menu message and keyboard back to main menu.

    :param callback: :class:`CallbackQuery`, from which comes the callback data (chat ID, message ID, etc.)
    :param bot: :class:`Bot` instance to delete and re-send the message with different inline keyboard and text
    :param state: :class:`FSMContext` to reset the state of the notification setup context
    :return: Returns :type:`None`, just does single action
    """

    await callback.answer()
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id) # type: ignore
    await bot.send_message(chat_id=callback.message.chat.id, text=MAIN_MENU, reply_markup=ADMIN_MAIN_MENU) # type: ignore
    await state.set_state(None)

class WaitForInput(StatesGroup):
    """
    This object represents a FSM state to infinetly accept some user's messages, until requirements met, or turned off.
    """

    entering_time = State()
    get_users_file = State()
    get_DB_file = State()
    """The entering state itself"""

@router.callback_query(F.data.startswith("update"))
async def get_updated_data(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """
    Handles the requests for data updates and directs their behavior.

    :param callback: :class:`CallbackQuery`, from which comes the callback data (request, chat ID, message ID, etc.)
    :param bot: :class:`Bot` instance for front-end work
    :param state: :class:`FSMContext` for reading/changing the FSM state of the router.
    :return: Returns :type:`None`, since not used anywhere else
    """

    function = callback.data.split(" ")[1] # type: ignore

    if function == "users":
        await callback.answer(reply_markup=RETURN_HOME)

        hint_pic = InputMediaPhoto(media=FSInputFile("message_media/users_table_struct.jpeg"), caption=SEND_ROLES_HINT)

        await bot.edit_message_media(chat_id=callback.message.chat.id, message_id=callback.message.message_id, media=hint_pic, reply_markup=RETURN_HOME) # type: ignore
        await state.set_state(WaitForInput.get_users_file)
    elif function == "DB":
        await callback.answer()
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text=SEND_INFO_HINT, reply_markup=RETURN_HOME) # type: ignore
        await state.set_state(WaitForInput.get_DB_file)

@router.message(StateFilter(WaitForInput.get_users_file))
async def get_users_file(msg: Message, state: FSMContext, bot: Bot) -> None:
    """
    Downloads the file containing users' roles. Or turns them around.

    :param msg: :class:`Message` that the user sent
    :param state: :class:`FSMContext` for reading/changing the FSM state of the router
    :param bot: :class:`Bot` instance for file handling
    :return: Returns :type:`None`, since no output produced.
    """

    if msg.content_type == "document":
        if not msg.document.file_name.endswith(".xlsx"): # type: ignore
            await msg.answer("Пожалуйста, отправьте ещё раз. Файл должен быть `.xlsx`")
        else:
            file = await bot.get_file(msg.document.file_id) # type: ignore

            await bot.download_file(file.file_path, config.STORAGE_FOLDER.get_secret_value() + "tgnames.xlsx") # type: ignore
            await state.set_state(None)
            await msg.answer("Отлично, обновляю доступ...")
            await SDH(Request.UPDATE_ROLES_DB)
            await msg.answer(MAIN_MENU, reply_markup=ADMIN_MAIN_MENU)
            await state.set_state(None)
    else:
        await msg.answer("Пожалуйста, отправьте ещё раз. Файл должен быть `.xlsx.")

@router.message(StateFilter(WaitForInput.get_DB_file))
async def get_DB_file(msg: Message, state: FSMContext, bot: Bot) -> None:
    """
    Downloads the file containing students' stats. Or turns them around.

    :param msg: :class:`Message` that the user sent
    :param state: :class:`FSMContext` for reading/changing the FSM state of the router
    :param bot: :class:`Bot` instance for file handling
    :return: Returns :type:`None`, since no output produced.
    """

    if msg.content_type == "document":
        if not re.match("kidp\_stats\_one\_excel\_\d{4}-\d{2}-\d{2}.xlsx", msg.document.file_name): # type: ignore
            await msg.answer("Пожалуйста, отправьте ещё раз. Файл должен быть `.xlsx`")
        else:
            file = await bot.get_file(msg.document.file_id) # type: ignore

            await bot.download_file(file.file_path, config.STORAGE_FOLDER.get_secret_value() + msg.document.file_name) # type: ignore
            await msg.answer("Отлично! База обновлена.")
            await SDH(Request.UPDATE_DATA_DB, msg.document.file_name) # type: ignore
            await msg.answer(MAIN_MENU, reply_markup=ADMIN_MAIN_MENU)
            await state.set_state(None)
    else:
        await msg.answer("Пожалуйста, отправьте ещё раз. Файл должен быть `.xlsx` и называться по шаблону _kidp\_stats\_one\_excel\_ГГГГ-ММ-ДД.xlsx_")

@router.callback_query(F.data == "notifications setup")
async def setup_notifications(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """
    Displays a menu to chose the weekday for the notifications.

    :param callback: :class:`CallbackQuery`, from which comes the callback data (chat ID, message ID, etc.)
    :param bot: :class:`Bot` instance for all the front-end work
    :param state: :class:`FSMContext` to reset the state of the notification setup context
    :return: Returns :type:`None`, since not used anywhere else
    """

    await callback.answer()

    SETUP_NOTIFICATIONS_MENU = await build_notifications_keyboard(callback.from_user.username, callback.message.chat.id) # type: ignore

    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text="Выберите день для настройки сообщений", reply_markup=SETUP_NOTIFICATIONS_MENU.as_markup()) # type: ignore
    await state.set_state(None)

@router.callback_query(F.data.startswith("selected"))
async def select_day(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """
    Reacts to when the weekday was chosen.

    :param callback: :class:`CallbackQuery`, from which comes the callback data (request, chat ID, message ID, etc.)
    :param bot: :class:`Bot`for all the front-end work
    :param state: :class:`FSMContext` to set the state an loop the input of the timestamps
    :return: Returns :type:`None`, since not used anywhere else
    """

    global day
    day = callback.data.split(" ")[1] # type: ignore
    notifications = await fetch_notifications(callback.from_user.username, callback.message.chat.id, day) # type: ignore
    answer_text = "Напишите время напоминания в формате *ЧЧ:ММ* для добавления/удаления напоминания\n\nВот уже установленные:\n"

    for notification in notifications:
        answer_text += (notification + "\n")

    await callback.answer()
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text=answer_text, reply_markup=SET_TIME_MENU) # type: ignore
    await state.set_state(WaitForInput.entering_time)

@router.message(StateFilter(WaitForInput.entering_time))
async def get_time(msg: Message) -> None:
    """
    Retrieves timestamps for user's messages.

    :param msg: :class:`Message` instance to get info from, and answer to them
    :return: Returns :type:`None`, since not used anywhere else
    """

    if re.match("\d{2}:\d{2}", msg.text): # type: ignore
        hrs, mins = msg.text.split(":") # type: ignore

        if int(hrs) > 23 or int(mins) > 59:
            await msg.answer("Неправильный формат: нужно _ЧЧ:ММ_", reply_markup=SET_TIME_MENU)
        else:
            global day

            notifications = await fetch_notifications(msg.from_user.username, msg.chat.id, day) # type: ignore

            if msg.text in notifications:
                await remove_notification(msg.from_user.username, day, msg.text) # type: ignore
                await msg.answer("Больше не буду уведомлять в {}, {}".format(msg.text, await translate_weekday(day)), reply_markup=SET_TIME_MENU)
            else:
                await msg.answer("Вы будете уведомлены в {}, {}".format(msg.text, await translate_weekday(day)), reply_markup=SET_TIME_MENU)
                await set_notification(msg.from_user.username, day, msg.text) # type: ignore
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