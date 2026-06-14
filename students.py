from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.formatting import Text
from middlewares import RoleFilter, Role

#region messages
GREETING = """
Привет! Я - бот для просмотра твоей статистики по учебным работам.
"""
#endregion

router = Router()
router.message.filter(RoleFilter(Role.STUDENT))

@router.message(Command("start"))
async def greet(msg: Message) -> None:
    """
    Greeting message for student-level users.

    :param msg: `Message` instance for a handler.
    :return: Returns `None`, just answers the _/start_ message
    """
    
    await msg.answer(**Text(GREETING).as_kwargs())