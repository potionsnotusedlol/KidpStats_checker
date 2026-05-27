from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

ADMIN_MAIN_MENU_LAYOUT = [
    [
        InlineKeyboardButton(text="🥤 Обновить информацию по пользователям", callback_data="update users"),
        InlineKeyboardButton(text="♿️ Обновить информацию по работам", callback_data="update DB")
    ],
    [InlineKeyboardButton(text="🂁 Настроить напоминания", callback_data="notifications setup")]
]
ADMIN_MAIN_MENU = InlineKeyboardMarkup(inline_keyboard=ADMIN_MAIN_MENU_LAYOUT)
SETUP_NOTIFICATIONS_MENU_LAYOUT = [
    [InlineKeyboardButton(text="Понедельник ❌", callback_data="selected monday")],
    [InlineKeyboardButton(text="Вторник ❌", callback_data="selected tuesday")],
    [InlineKeyboardButton(text="Среда ❌", callback_data="selected wendesday")],
    [InlineKeyboardButton(text="Четверг ❌", callback_data="selected thursday")],
    [InlineKeyboardButton(text="Пятница ✅", callback_data="selected friday")],
    [InlineKeyboardButton(text="Суббота ❌", callback_data="selected saturday")],
    [InlineKeyboardButton(text="Воскресенье ❌", callback_data="selected sunday")]
]
SETUP_NOTIFICATIONS_MENU = InlineKeyboardMarkup(inline_keyboard=SETUP_NOTIFICATIONS_MENU_LAYOUT)