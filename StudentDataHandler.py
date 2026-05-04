from enum import IntEnum
from functools import wraps

import aiosqlite

async def initDB(path_to_database):
    async with aiosqlite.connect(path_to_database) as role_database:
        await role_database.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id TEXT PRIMARY KEY,
            fullname TEXT NOT NULL
        )
        """)
        await role_database.commit()

# region roles handling
async def getUserRole(user_id, path_to_database):
    async with aiosqlite.connect(path_to_database) as role_database:
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
            return 3
        elif role == "admin":
            return 2
        elif role != "admin" and role != "owner":
            return 1
    else:
        return 0    
# endregion

# region RBAC implementation
class Role(IntEnum):
    GUEST = 0
    STUDENT = 1
    ADMIN = 2
    OWNER = 3

def requireAcess(role: Role):
    def decorator(func):
        @wraps(func)
        async def wrapper():
            pass

# endregion