from aiogram import Router
from aiogram.filters import Command
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from config import ADMIN_ID
from database import get_pending_deposits

router = Router()


@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "👮‍♂️ Admin Panel\n\n"
        "Commands:\n"
        "/pending - Pending Deposit List"
    )


@router.message(Command("pending"))
async def pending_deposits(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    deposits = await get_pending_deposits()

    if not deposits:
        await message.answer("✅ কোনো Pending Deposit নেই।")
        return

    for deposit in deposits:
        deposit_id, user_id, amount, trxid, screenshot = deposit

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✅ Approve",
                        callback_data=f"approve:{deposit_id}"
                    ),
                    InlineKeyboardButton(
                        text="❌ Reject",
                        callback_data=f"reject:{deposit_id}"
                    ),
                ]
            ]
        )

        await message.bot.send_photo(
            chat_id=message.chat.id,
            photo=screenshot,
            caption=(
                f"📥 Deposit ID: {deposit_id}\n\n"
                f"👤 User ID: {user_id}\n"
                f"💰 Amount: {amount} Tk\n"
                f"🔑 TrxID: {trxid}"
            ),
            reply_markup=keyboard,
        )
