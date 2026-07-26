from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message(lambda message: message.text == "📥 Deposit")
async def deposit(message: Message):
    await message.answer(
        "💳 Manual Deposit\n\n"
        "📱 bKash (Personal): 01330930330\n"
        "📱 Nagad (Personal): 01841245373\n\n"
        "📝 টাকা পাঠানোর পর আপনার:\n"
        "1. Amount\n"
        "2. Transaction ID (TrxID)\n"
        "3. Payment Screenshot\n\n"
        "অ্যাডমিনের কাছে পাঠান।"
    )
