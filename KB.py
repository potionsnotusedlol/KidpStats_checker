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
WEEKDAYS = {
    "monday": "Понедельник ",
    "tuesday": "Вторник ",
    "wendesday": "Среда ",
    "thursday": "Четверг ",
    "friday": "Пятница ",
    "saturday": "Суббота ",
    "sunday": "Воскресенье "
}

# rewrite later to another file
async def translateWeekday(weekday: str):
    return WEEKDAYS[weekday]

async def initNotificationsFile():
    file_path = STORAGE_DIR + "notifications.json"

    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        with open(file_path, "w") as F:
            total = {"users": []}

            json.dump(total, F, indent=4)

async def initUserNotifications(username: str, chat_id: int):
    with open(STORAGE_DIR + "notifications.json", "r") as F:
        content = json.load(F)
        new_data = {
            "username": username,
            "chat_id": chat_id,
            "times": []
        }

        content["users"].append(new_data)
    
    with open(STORAGE_DIR + "notifications.json", "w") as F:
        json.dump(content, F, indent=4)

async def fetchNotifications(username: str, chat_id: int, weekday: str) -> list:
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
        
    await initUserNotifications(username, chat_id)

    return []

def loadAllUsers() -> list[tuple]:
    with open(STORAGE_DIR + "notifications.json", "r") as F:
        data = json.load(F)

    return [(user["username"], user["chat_id"]) for user in data["users"]]

async def setNotification(username: str, weekday: str, time: str):
    time_to_set = {weekday: time}

    print(time_to_set)

    with open(STORAGE_DIR + "notifications.json", "r") as F:
        total = json.load(F)

        for i in total["users"]:
            if i["username"] == username:
                weekday_times = [
                    time_dict
                    for time_dict in i["times"]
                ]

        weekday_times.append(time_to_set)

        print(weekday_times)
        
        seen = set()
        final_times = []

        for d in weekday_times:
            t = tuple(d.items())

            if t not in seen:
                seen.add(t)
                final_times.append(d)

    with open(STORAGE_DIR + "notifications.json", "w") as F:
        for i in total["users"]:
            if i["username"] == username:
                i["times"] = final_times
        
        json.dump(total, F, indent=4)


async def buildNotificationsKeyboard(username: str, chat_id: int) -> InlineKeyboardBuilder:
    SETUP_NOTIFICATIONS_MENU = InlineKeyboardBuilder()

    for eng, rus in WEEKDAYS.items():
        cd = "selected " + eng
        check = await fetchNotifications(username, chat_id, eng)

        if check == []:
            txt = rus + "❌"

            SETUP_NOTIFICATIONS_MENU.row(InlineKeyboardButton(text=txt, callback_data=cd))
        else:
            txt = rus + "✅"

            SETUP_NOTIFICATIONS_MENU.row(InlineKeyboardButton(text=txt, callback_data=cd))
        
    SETUP_NOTIFICATIONS_MENU.row(InlineKeyboardButton(text="Вернуться в главное меню 🎽", callback_data="menus"))

    return SETUP_NOTIFICATIONS_MENU

SET_TIME_MENU_LAYOUT = [[
    InlineKeyboardButton(text="Назад ⏪", callback_data="notifications setup"),
    InlineKeyboardButton(text="Меню 🌥️", callback_data="menus")
]]
SET_TIME_MENU = InlineKeyboardMarkup(inline_keyboard=SET_TIME_MENU_LAYOUT)