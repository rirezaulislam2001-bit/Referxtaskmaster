from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import WithdrawState
from config import ADMIN_ID
from database import get_balance, save_withdraw

router = Router()


@router.message(lambda message: message.text == "💸 Withdraw")
async def withdraw_start(message: Message, state: FSMContext):
    balance = await get_balance(message.from_user.id)

    if balance <= 0:
        await message.answer(
            "❌ আপনার Balance 0 Tk.\nWithdraw করা সম্ভব নয়।"
        )
        return

    await state.set_state(WithdrawState.amount)

    await message.answer(
        f"💰 আপনার বর্তমান Balance: {balance} Tk\n\n"
        "কত টাকা Withdraw করতে চান?"
    )


@router.message(WithdrawState.amount)
async def get_amount(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ শুধু সংখ্যা লিখুন।")
        return

    balance = await get_balance(message.from_user.id)
    amount = int(message.text)

    if amount > balance:
        await message.answer(
            f"❌ আপনার Balance মাত্র {balance} Tk।"
        )
        return

    await state.update_data(amount=amount)
    await state.set_state(WithdrawState.method)

    await message.answer(
        "💳 কোন মাধ্যমে Withdraw নিতে চান?\n\n"
        "লিখুন:\n"
        "bKash\n"
        "অথবা\n"
        "Nagad"
    )


@router.message(WithdrawState.method)
async def get_method(message: Message, state: FSMContext):
    method = message.text.strip()

    if method.lower() not in ["bkash", "nagad"]:
        await message.answer(
            "❌ শুধু bKash অথবা Nagad লিখুন।"
        )
        return

    await state.update_data(method=method)
    await state.set_state(WithdrawState.number)

    await message.answer("📱 আপনার Payment Number লিখুন।")


@router.message(WithdrawState.number)
async def get_number(message: Message, state: FSMContext):
    data = await state.get_data()

    # Database-এ Withdraw Save
    await save_withdraw(
        user_id=message.from_user.id,
        amount=data["amount"],
        method=data["method"],
        number=message.text,
    )

    # Admin Notification
    await message.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            "💸 নতুন Withdraw Request\n\n"
            f"👤 Name: {message.from_user.full_name}\n"
            f"🆔 User ID: {message.from_user.id}\n"
            f"💰 Amount: {data['amount']} Tk\n"
            f"💳 Method: {data['method']}\n"
            f"📱 Number: {message.text}"
        )
    )

    await message.answer(
        "✅ আপনার Withdraw Request গ্রহণ করা হয়েছে।\n"
        "Admin যাচাই করার পর Payment পাঠানো হবে।"
    )

    await state.clear()
