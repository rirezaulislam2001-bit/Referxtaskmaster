from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import DepositState
from config import ADMIN_ID
from database import save_deposit

router = Router()


@router.message(lambda message: message.text == "📥 Deposit")
async def deposit_start(message: Message, state: FSMContext):
    await state.set_state(DepositState.amount)
    await message.answer(
        "💰 আপনি কত টাকা ডিপোজিট করেছেন?\n\nশুধু সংখ্যাটি লিখুন।"
    )


@router.message(DepositState.amount)
async def get_amount(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ শুধু সংখ্যা লিখুন।")
        return

    await state.update_data(amount=int(message.text))
    await state.set_state(DepositState.trxid)

    await message.answer("🆔 এখন আপনার Transaction ID (TrxID) লিখুন।")


@router.message(DepositState.trxid)
async def get_trxid(message: Message, state: FSMContext):
    await state.update_data(trxid=message.text)
    await state.set_state(DepositState.screenshot)

    await message.answer("📷 এখন পেমেন্টের Screenshot পাঠান।")


@router.message(DepositState.screenshot)
async def get_screenshot(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("❌ অনুগ্রহ করে Screenshot পাঠান।")
        return

    data = await state.get_data()

    screenshot = message.photo[-1].file_id

    await save_deposit(
        user_id=message.from_user.id,
        amount=data["amount"],
        trxid=data["trxid"],
        screenshot=screenshot
    )

    await message.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=screenshot,
        caption=(
            "📥 নতুন Deposit Request\n\n"
            f"👤 Name: {message.from_user.full_name}\n"
            f"🆔 User ID: {message.from_user.id}\n"
            f"💰 Amount: {data['amount']} Tk\n"
            f"🔑 TrxID: {data['trxid']}"
        )
    )

    await message.answer(
        "✅ আপনার Deposit Request সফলভাবে জমা হয়েছে।\n\n"
        "অ্যাডমিন যাচাই করার পর Balance যোগ করা হবে।"
    )

    await state.clear()
