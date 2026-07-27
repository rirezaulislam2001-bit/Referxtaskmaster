from aiogram import Router
from aiogram.types import Message
from config import ADMIN_ID

router = Router()

@router.message(lambda message: message.from_user.id == ADMIN_ID and message.text == "/admin")
async def admin_panel(message: Message):
    await message.answer(
        "👮 Admin Panel\n\n"
        "✅ Admin Panel চালু হয়েছে।"
    )
