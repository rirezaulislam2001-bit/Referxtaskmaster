from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage

import asyncio
import os

from database import init_db
from handlers.deposit import router as deposit_router

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👤 Profile"), KeyboardButton(text="👥 Refer")],
        [KeyboardButton(text="📋 Tasks"), KeyboardButton(text="💰 Balance")],
        [KeyboardButton(text="📥 Deposit"), KeyboardButton(text="💸 Withdraw")],
    ],
    resize_keyboard=True
)


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "🎉 REFERXTASKMASTER_BOT-এ স্বাগতম!",
        reply_markup=menu
    )


async def main():
    await init_db()

    # Deposit Router
    dp.include_router(deposit_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
