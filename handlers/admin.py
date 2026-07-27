from aiogram import Router
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from config import ADMIN_ID
from database import (
    get_pending_deposits,
    get_deposit,
    approve_deposit,
    add_balance,
)

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


@router.callback_query(lambda c: c.data.startswith("approve:"))
async def approve_callback(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ আপনি Admin নন।", show_alert=True)
        return

    deposit_id = int(callback.data.split(":")[1])

    deposit = await get_deposit(deposit_id)

    if deposit is None:
        await callback.answer("❌ Deposit পাওয়া যায়নি।", show_alert=True)
        return

    user_id, amount, status = deposit

    if status == "approved":
        await callback.answer("⚠️ এই Deposit আগে থেকেই Approved।")
        return

    await approve_deposit(deposit_id)
    await add_balance(user_id, amount)

    await callback.bot.send_message(
        user_id,
        f"🎉 আপনার Deposit Approved হয়েছে!\n\n"
        f"💰 {amount} Tk আপনার Balance-এ যোগ করা হয়েছে।"
    )

    await callback.message.edit_caption(
        caption=callback.message.caption + "\n\n✅ APPROVED"
    )

    await callback.answer("✅ Deposit Approved")
