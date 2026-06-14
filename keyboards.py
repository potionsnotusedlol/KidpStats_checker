from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import config
from admins.notifications import WEEKDAYS, fetch_notifications

STORAGE_DIR=config.STORAGE_FOLDER.get_secret_value()
ADMIN_MAIN_MENU_LAYOUT = [
    [
        InlineKeyboardButton(text="🥤 Обновить информацию по пользователям", callback_data="update users"),
        InlineKeyboardButton(text="♿️ Обновить информацию по работам", callback_data="update DB")
    ],
    [InlineKeyboardButton(text="🂁 Настроить напоминания", callback_data="notifications setup")]
]
ADMIN_MAIN_MENU = InlineKeyboardMarkup(inline_keyboard=ADMIN_MAIN_MENU_LAYOUT)
RETURN_HOME_LAYOUT = [[InlineKeyboardButton(text="В главное меню🚀", callback_data="menus")]]
RETURN_HOME = InlineKeyboardMarkup(inline_keyboard=RETURN_HOME_LAYOUT)
SET_TIME_MENU_LAYOUT = [[
    InlineKeyboardButton(text="Назад ⏪", callback_data="notifications setup"),
    InlineKeyboardButton(text="Меню 🌥️", callback_data="menus")
]]
SET_TIME_MENU = InlineKeyboardMarkup(inline_keyboard=SET_TIME_MENU_LAYOUT)

async def build_notifications_keyboard(username: str, chat_id: int) -> InlineKeyboardBuilder:
    """
    Builds a keyboard that displays whether the weekday contains a notification entry.

    :param username: 
    """

    SETUP_NOTIFICATIONS_MENU = InlineKeyboardBuilder()

    for eng, rus in WEEKDAYS.items():
        cd = "selected " + eng
        check = await fetch_notifications(username, chat_id, eng)

        if check == []:
            txt = rus + "❌"

            SETUP_NOTIFICATIONS_MENU.row(InlineKeyboardButton(text=txt, callback_data=cd))
        else:
            txt = rus + "✅"

            SETUP_NOTIFICATIONS_MENU.row(InlineKeyboardButton(text=txt, callback_data=cd))
        
    SETUP_NOTIFICATIONS_MENU.row(InlineKeyboardButton(text="Вернуться в главное меню 🎽", callback_data="menus"))

    return SETUP_NOTIFICATIONS_MENU