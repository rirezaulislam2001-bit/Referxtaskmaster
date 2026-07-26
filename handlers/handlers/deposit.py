from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import DepositState

router = Router()

@router.message(lambda message: message.text == "📥 Deposit")
async def deposit_start(message: Message, state: FSMContext):
    await state.set_state(DepositState.amount)
    await message.answer("💰 আপনি কত টাকা ডিপোজিট করেছেন? (শুধু সংখ্যা লিখুন)")
@router.message(DepositState.amount)
async def get_amount(message: Message, state: FSMContext):
    await state.update_data(amount=message.text)
    await state.set_state(DepositState.trxid)
    await message.answer("🆔 এখন আপনার Transaction ID (TrxID) লিখুন:")
@router.message(DepositState.trxid)
async def get_trxid(message: Message, state: FSMContext):
    await state.update_data(trxid=message.text)
    await state.set_state(DepositState.screenshot)
    await message.answer(
        "📷 এখন আপনার পেমেন্টের Screenshot পাঠান।"
    )@router.message(DepositState.screenshot)
async def get_screenshot(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("❌ অনুগ্রহ করে একটি Screenshot পাঠান।")
        return

    data = await state.get_data()

    await message.answer(
        "✅ আপনার Deposit Request সফলভাবে জমা হয়েছে।\n"
        "অ্যাডমিন যাচাই করার পর আপনার ব্যালেন্স আপডেট করা হবে।"
    )

    await state.clear()
