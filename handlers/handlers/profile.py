from aiogram import Router
from aiogram.types import Message

from database import get_balance

router = Router()


@router.message(lambda message: message.text == "👤 Profile")
async def profile(message: Message):
    balance = await get_balance(message.from_user.id)

    await message.answer(
        f"👤 Profile\n\n"
        f"📝 Name: {message.from_user.full_name}\n"
        f"🆔 User ID: {message.from_user.id}\n"
        f"💰 Balance: {balance} Tk"
    )


@router.message(lambda message: message.text == "💰 Balance")
async def balance(message: Message):
    balance = await get_balance(message.from_user.id)

    await message.answer(
        f"💰 আপনার বর্তমান Balance: {balance} Tk"
    )
