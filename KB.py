from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

admin_main_menu = InlineKeyboardBuilder()

admin_main_menu.row(InlineKeyboardButton(text="🥤 Обновить информацию по пользователям", callback_data="update users"), InlineKeyboardButton(text="♿️ Обновить информацию по работам", callback_data="update DB"))
admin_main_menu.row(InlineKeyboardButton(text="🂁 Настроить напоминания", callback_data="notifications setup"))