from aiogram.types import Message
from aiogram import types, Router, F
from aiogram.filters import Command, CommandStart
from ..Text import START_MESSAGE, INSTRUMENTS_LIST
from Main_bot.utils.binance_api import pull_of_instruments, get_currency_info
from Main_bot.keyboards.mainkeyboard import keyboard_main_commands,keyboard_currency_list
from Main_bot.states.states_main import CurrencyState
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(Command('start'))
async def start_handler(message:Message):
    await message.answer(START_MESSAGE,reply_markup=keyboard_main_commands)

@router.message(F.text=='Get general exchange information')
async def chose_instrument(message:Message, state:FSMContext):
    await message.answer(INSTRUMENTS_LIST,reply_markup=keyboard_currency_list)
    await state.set_state(CurrencyState.CHOOSE_CURRENCY)

@router.message(CurrencyState.CHOOSE_CURRENCY,F.text.in_(pull_of_instruments))
async def get_exchange_info(message: Message,state:FSMContext):
    symbol = message.text
    await state.update_data(currency = symbol)
    await message.answer(get_currency_info(symbol))

