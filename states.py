from aiogram.fsm.state import State, StatesGroup


class DepositState(StatesGroup):
    amount = State()
    trxid = State()
    screenshot = State()


class WithdrawState(StatesGroup):
    amount = State()
    method = State()
    number = State()
