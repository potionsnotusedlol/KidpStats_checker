from enum import IntEnum
from functools import wraps
from Config import config
from aiogram.types import Message

import aiosqlite
import re

roles_db_path = config.ROLES_DB_PATH.get_secret_value()

class Role(IntEnum):
    GUEST = 0
    STUDENT = 1
    ADMIN = 2
    OWNER = 3

# region DB handling
async def getUserRole(user_id) -> Role:
    async with aiosqlite.connect(roles_db_path) as role_database:
        async with role_database.execute("""
        SELECT 1
        FROM Users
        WHERE id = ?
        LIMIT 1
        """,
        (user_id)
        ) as cursor:
            role = await cursor.fetchone()

    # a little bit of shitty if's in here))
    if role is not None:
        if role == "owner":
            return Role.OWNER
        elif role == "admin":
            return Role.ADMIN
        elif role != "admin" and role != "owner":
            return Role.STUDENT
        
    return Role.GUEST
# endregion

# region RBAC implementation

def requireAcess(req_role: Role):
    def decorator(func):
        @wraps(func)
        async def wrapper(msg: Message):
            uid = msg.from_user.username # type: ignore
            role = await getUserRole(uid)

            if role < req_role:
                return
            
            return await func(msg)
        return wrapper
    return decorator

class Request(IntEnum):
    UPDATE_ROLES_DB = 0
    UPDATE_DATA_DB = 1

def SDH(request: Request, uid: str):
    if request == Request.UPDATE_ROLES_DB:

            

# endregion