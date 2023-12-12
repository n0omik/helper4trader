import asyncio
from aiogram.types import Message
from aiogram import types, Router, F
from aiogram.filters import Command, CommandStart
from ..Text import START_MESSAGE, INSTRUMENTS_LIST, TIMEFRAME_LIST, PROJECT_INFO
from Main_bot.utils.openai_api import get_project_info_openai
from Main_bot.utils.binance_api import pull_of_instruments, get_currency_info, timeframe_reterned
from Main_bot.keyboards.mainkeyboard import keyboard_main_commands,keyboard_currency_list, keyboard_timeframes_list
from Main_bot.states.states_main import CurrencyState
from aiogram.fsm.context import FSMContext
from ..keyboards.pagenation import ReplyKeyboardPaginator


pagination_keyboard = ReplyKeyboardPaginator(pull_of_instruments)

router = Router()
router.include_router(pagination_keyboard.get_pagination_handler())
@router.message(Command('start'))
async def start_handler(message:Message):
    await message.answer(START_MESSAGE,reply_markup=keyboard_main_commands)

@router.message(F.text=='Get general exchange information for coin')
async def chose_instrument(message:Message, state:FSMContext):
    await message.answer(INSTRUMENTS_LIST,reply_markup=pagination_keyboard.get_keyboard())
    await state.set_state(CurrencyState.CHOOSE_CURRENCY)

@router.message(CurrencyState.CHOOSE_CURRENCY,F.text.in_(pull_of_instruments))
async def get_exchange_info(message: Message,state:FSMContext):
    symbol = message.text
    await state.set_state(CurrencyState.CHOOSE_TIMEFRAME)
    await message.answer(TIMEFRAME_LIST, reply_markup=keyboard_timeframes_list)
    await state.update_data(currency = symbol)

@router.message(CurrencyState.CHOOSE_TIMEFRAME,F.text.in_(timeframe_reterned))
async def get_exchange_info(message: Message, state: FSMContext):
    await message.answer(text='Please wait for a response. This may take up to 15 seconds.')
    timeframe = message.text
    data = await state.get_data()
    symbol = data.get('currency', None)
    await state.update_data(timeframe = timeframe)
    await message.answer(get_currency_info(symbol,timeframe_reterned.get(timeframe)))

@router.message(F.text=='Get general project information for coin')
async def get_project_info_keyboard(message:Message, state:FSMContext):
    await message.answer(PROJECT_INFO,reply_markup=keyboard_currency_list)
    await state.set_state(CurrencyState.CHOOSE_PROJECT)

@router.message(CurrencyState.CHOOSE_PROJECT, F.text.in_(pull_of_instruments))
async def get_project_info(message: Message, state: FSMContext):
    symbol = message.text
    await message.answer(text='Please wait for a response, we ask for an AI response to be prepared. This may take up to 1 minute.')
    await state.get_data()
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, lambda: asyncio.run(get_project_info_openai(symbol)))
    await message.answer(result)
    