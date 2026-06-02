from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from Config import config

import json
import os

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
# SETUP_NOTIFICATIONS_MENU = InlineKeyboardBuilder()
WEEKDAYS = {
    "monday": "Понедельник ",
    "tuesday": "Вторник ",
    "wendesday": "Среда ",
    "thursday": "Четверг ",
    "friday": "Пятница ",
    "saturday": "Суббота ",
    "sunday": "Воскресенье "
}

async def initNotificationsFile():
    file_path = STORAGE_DIR + "notifications.json"

    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        with open(file_path, "w") as F:
            total = {"users": []}

            json.dump(total, F, indent=4)

async def initUserNotifications(username: str):
    with open(STORAGE_DIR + "notifications.json", "r") as F:
        content = json.load(F)
        new_data = {
            "username": username,
            "times": []
        }

        content["users"].append(new_data)
    
    with open(STORAGE_DIR + "notifications.json", "w") as F:
        json.dump(content, F, indent=4)

async def fetchNotifications(username: str, weekday: str) -> list:
    with open(STORAGE_DIR + "notifications.json", "r") as F:
        total = json.load(F)

        for i in total["users"]:
            if i["username"] == username:
                weekday_times = [
                    time_dict[weekday]
                    for time_dict in i["times"]
                    if weekday in time_dict
                ]
                
                return weekday_times
        
    await initUserNotifications(username)

    return []

async def buildNotificationsKeyboard(username: str) -> InlineKeyboardBuilder:
    SETUP_NOTIFICATIONS_MENU = InlineKeyboardBuilder()

    for eng, rus in WEEKDAYS.items():
        cd = "selected " + eng
        check = await fetchNotifications(username, eng)

        if check == []:
            txt = rus + "❌"

            SETUP_NOTIFICATIONS_MENU.row(InlineKeyboardButton(text=txt, callback_data=cd))
        else:
            txt = rus + "✅"

            SETUP_NOTIFICATIONS_MENU.row(InlineKeyboardButton(text=txt, callback_data=cd))
        
    SETUP_NOTIFICATIONS_MENU.row(InlineKeyboardButton(text="Вернуться в главное меню 🎽", callback_data="menus"))

    return SETUP_NOTIFICATIONS_MENU