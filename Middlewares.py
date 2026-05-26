from collections.abc import Awaitable, Callable
from typing import Any, Callable
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from Config import config
from enum import IntEnum
from aiogram.filters import BaseFilter

import aiosqlite

ROLES_DB_PATH = config.STORAGE_FOLDER.get_secret_value() + config.ROLES_DB_NAME.get_secret_value()

class Role(IntEnum):
    GUEST = 0
    STUDENT = 1
    ADMIN = 2
    OWNER = 3

class InitMiddleware(BaseMiddleware):
    async def getUserRole(self, user_id) -> Role:
        if user_id == config.OWNER_USERNAME.get_secret_value():
            print("Got role for:", user_id, "-> OWNER")

            return Role.OWNER
    
        async with aiosqlite.connect(ROLES_DB_PATH) as role_database:
            async with role_database.execute(
                """
                    SELECT fullname
                    FROM Users
                    WHERE telegram_ID = ?
                    LIMIT 1
                """,
                (user_id,)
            ) as cursor:
                role = await cursor.fetchone()

        # a little bit of shitty if's in here))
        if role is not None:
            if role == "admin":
                print("Got role for:", user_id, "-> ADMIN")

                return Role.ADMIN
            elif role != "admin" and role != "owner":
                print("Got role for:", user_id, "-> STUDENT")

                return Role.STUDENT
        
        print("Got role for:", user_id, "-> GUEST")

        return Role.GUEST

    async def __call__(self, handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]], event: TelegramObject, data: dict[str, Any]) -> Any: # type: ignore
        actual_event = data.get("event_from_user")

        if actual_event:
            data["user_role"] = await self.getUserRole(actual_event.username)

        return await handler(event, data)
    
class RoleFilter(BaseFilter):
    def __init__(self, *roles: Role) -> None:
        self.roles = roles

    async def __call__(self, msg: Message, user_role: Role = Role.GUEST) -> bool:
        return user_role in self.roles