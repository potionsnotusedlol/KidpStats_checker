from aiogram import Router
from Middlewares import RoleFilter, Role
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()
router.message.filter(RoleFilter(Role.GUEST))

@router.message(CommandStart)
async def goodbye(msg: Message):
    await msg.answer("Бот в разработке, больше не приходи)")