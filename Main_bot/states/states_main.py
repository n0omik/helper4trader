from aiogram.fsm.state import StatesGroup, State

class CurrencyState(StatesGroup):
    CHOOSE_COMMAND = State()
    CHOOSE_CURRENCY = State()
    CHOOSE_TIMEFRAME = State()
    CHOOSE_PROJECT = State()
    SET_ALERT = State()
    SET_ALERT_PRICE = State()