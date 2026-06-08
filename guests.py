from aiogram import Router
from middlewares import RoleFilter, Role
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()
router.message.filter(RoleFilter(Role.GUEST))

@router.message(CommandStart)
async def goodbye(msg: Message) -> None:
    """
    Makes sure no one unrelated to the bot can have access.

    :param msg: `Message` instance for a handler.
    :return: Returns `None`, just answers the _/start_ message
    """
    
    await msg.answer("Бот в разработке, больше не приходи)")