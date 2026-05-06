from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

admin_main_menu = [
    [InlineKeyboardButton(text="🥤 Обновить информацию по пользователям", callback_data="update user info"),
     InlineKeyboardButton(text="♿️ Обновить информацию по работам", callback_data="update workind DB")],
    [InlineKeyboardButton(text="🂁 Настроить напоминания")]
]
admin_main_menu = InlineKeyboardMarkup(inline_keyboard=admin_main_menu)
