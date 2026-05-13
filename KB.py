from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

admin_main_menu = InlineKeyboardBuilder()

admin_main_menu.row(InlineKeyboardButton(text="🥤 Обновить информацию по пользователям", callback_data="update user info"), InlineKeyboardButton(text="♿️ Обновить информацию по работам", callback_data="update working DB"))
admin_main_menu.row(InlineKeyboardButton(text="🂁 Настроить напоминания", callback_data="notifications setup"))