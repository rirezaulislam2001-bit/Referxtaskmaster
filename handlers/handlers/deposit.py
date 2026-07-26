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
