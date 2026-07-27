from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage

import asyncio
import os

from database import init_db, add_user
from handlers.deposit import router as deposit_router
from handlers.admin import router as admin_router

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
    # User-কে Database-এ Save করবে
    await add_user(message.from_user.id)

    await message.answer(
        "🎉 REFERXTASKMASTER_BOT-এ স্বাগতম!",
        reply_markup=menu
    )


async def main():
    # Database তৈরি
    await init_db()

    # Routers
    dp.include_router(deposit_router)
    dp.include_router(admin_router)

    # Bot Start
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
