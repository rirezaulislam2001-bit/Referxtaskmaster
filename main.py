from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
import asyncio
import os
from database import init_db
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

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
@dp.message(lambda message: message.text == "📥 Deposit")
async def deposit(message: Message):
    await message.answer(
        "💳 Manual Deposit\n\n"
        "📱 bKash (Personal): 01330930330\n"
        "📱 Nagad (Personal): 01841245373\n\n"
        "✅ টাকা পাঠানোর পর আপনার Transaction ID (TrxID) এবং Screenshot অ্যাডমিনকে পাঠান।\n\n"
        "👤 Admin: @referxtaskmaster"
    )
async def main():
    await init_db()
    await dp.start_polling(bot)
    a

if __name__ == "__main__":
    asyncio.run(main())
