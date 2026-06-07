from aiogram import Bot
from asyncio import sleep
from datetime import datetime
from config import config

import os
import json

WEEKDAYS = {
    "monday": "Понедельник ",
    "tuesday": "Вторник ",
    "wendesday": "Среда ",
    "thursday": "Четверг ",
    "friday": "Пятница ",
    "saturday": "Суббота ",
    "sunday": "Воскресенье "
}
FILE_PATH = config.STORAGE_FOLDER.get_secret_value() + "notifications.json"

async def translate_weekday(weekday: str) -> str:
    """
    Gets russian weekday name for an english entry.

    :param weekday: String key value to access `WEEKDAYS` dictionary
    :return: Returns :type:`str` value of a russian equivalent to the weekday
    """

    return WEEKDAYS[weekday]

async def init_notifications_file() -> None:
    """
    Initializes notifications file when the bot is freshly started, or something happened to it.

    :return: Returns :type:`None`, because it just makes the file with no output
    """

    if not os.path.exists(FILE_PATH) or os.path.getsize(FILE_PATH) == 0:
        with open(FILE_PATH, "w") as F:
            total = {"users": []}

            json.dump(total, F, indent=4)

async def init_user_notifications(username: str, chat_id: int) -> None:
    """
    Initializes an empty array for new user's notifications timestamps, if not already existing.

    :param username: username key to get access to notifications data, in the format :code:`username`
    :param chat_id: Chat ID key from the chat that the user is on, used to get the chat to send notifications to
    :return: Returns :type:`None`, since has no output for other objects to get
    """

    with open(FILE_PATH, "r") as F:
        content = json.load(F)
        new_data = {
            "username": username,
            "chat_id": chat_id,
            "times": []
        }

        content["users"].append(new_data)
    
    with open(FILE_PATH, "w") as F:
        json.dump(content, F, indent=4)

async def fetch_notifications(username: str, chat_id: int, weekday: str) -> list:
    """
    Fetches notifications for a specific day for a user.

    :param username: username key to get access to notifications data
    :param chat_id: Chat ID key to get access to notifications data
    :param weekday: specific day to fetch the timestamps for
    :return: Returns :type:`list[dict]` containing all the timestamps, or empty array if no notifications were set before
    """

    with open(FILE_PATH, "r") as F:
        total = json.load(F)

        for i in total["users"]:
            if i["username"] == username:
                weekday_times = [
                    time_dict[weekday]
                    for time_dict in i["times"]
                    if weekday in time_dict
                ]

                return weekday_times
            
    await init_user_notifications(username, chat_id)

    return []

def load_all_users() -> list[tuple]:
    """
    Gets all the usernames and all the corresponding chat IDs.

    :return: Returns a list of pairs of usernames and chat IDs, represented in tuple for more convenient operations
    """

    with open(FILE_PATH, "r") as F:
        data = json.load(F)

    return [(user["username"], user["chat_id"]) for user in data["users"]]

async def set_notification(username: str, weekday: str, time: str) -> None:
    """
    Places new timestamp entry in a .json file. Also checks there are no doubling/collisions.

    :param username: Telegram username in the format :code:`username`
    :param weekday: Day of the week to assign to, strictly standardized
    :param time: :type:`str` value of a timestamp in the format :code:`HH:MM`
    :return: Returns :type:`None`, no output from the function
    """

    time_to_set = {weekday: time}

    print(time_to_set)

    with open(FILE_PATH, "r") as F:
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

    with open(FILE_PATH, "w") as F:
        for i in total["users"]:
            if i["username"] == username:
                i["times"] = final_times

        json.dump(total, F, indent=4)

async def send_notification(bot: Bot, chat_id: int, message: str) -> None:
    """
    Handle the bot seding one scheduled message.

    :param bot: Bot istance to indentify a chat to send to
    :param chat_id: numerical ID of a chat to send to
    :param message: text of a message to send
    :return: Returns :type:`None`, all the the function does is automatically send a message to a determined chat
    """

    try:
        chat = await bot.get_chat(chat_id)

        await bot.send_message(chat_id=chat.id, text=message)
    except Exception as e:
        print(f"Scheduled task malfunction: {e}")

async def notify(bot: Bot) -> None:
    """
    Dispatch all the notifications to users.

    :param bot: Bot instance to pass to the `send_notifications` function
    :return: Returns :type:`None`, all the functions does is fetch notifications and send them to the users' chats
    """

    now = datetime.now()
    curr_time = now.strftime("%H:%M")
    curr_weekday = now.strftime("%A").lower()

    for username, chat_id in load_all_users():
        times = await fetch_notifications(username, chat_id, curr_weekday)

        if curr_time in times:
            print("Notifying at", curr_weekday, curr_time, "for", username)
            await send_notification(bot, chat_id, "‼️Напоминаю обновить базу по результатам‼️")

async def run_scheduler(bot: Bot) -> None:
    """
    Check every minute for a message to send and conduct the notification if needed.

    :param bot: Bot instance to pass to `notify` function
    :return: Returns :type:`None`, it runs endlessly
    """

    # 25-second delay to let all the data to load without errors
    await sleep(25)

    while True:
        await notify(bot)

        now = datetime.now()

        print(f"Schedule running {now.hour}:{now.minute}:{now.second}")

        delay = 60 - now.second

        await sleep(delay)