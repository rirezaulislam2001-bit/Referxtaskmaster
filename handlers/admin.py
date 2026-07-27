from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import ADMIN_ID

router = Router()


@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "👮‍♂️ Admin Panel\n\n"
        "📥 Pending Deposits\n"
        "💰 Manage Balance\n"
        "👥 Manage Users\n\n"
        "✅ Admin Panel চালু হয়েছে।"
    )
