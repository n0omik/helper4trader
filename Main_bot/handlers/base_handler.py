import asyncio
import json
from aiogram.types import Message, CallbackQuery
from aiogram import types, Router, F, Bot
from aiogram.filters import Command, CommandStart
from ..Text import START_MESSAGE, INSTRUMENTS_LIST, TIMEFRAME_LIST, PROJECT_INFO, SET_ALERT
from Main_bot.utils.openai_api import get_project_info_openai
from Main_bot.utils.binance_api import pull_of_instruments, get_currency_info, timeframe_reterned, CoinAlert
from Main_bot.keyboards.mainkeyboard import keyboard_main_commands, keyboard_currency_list, keyboard_timeframes_list, \
    alet_direction_keyboard
from Main_bot.states.states_main import CurrencyState
from aiogram.fsm.context import FSMContext
from ..keyboards.pagination import ReplyKeyboardPaginator
from ..utils.redis_storage import storage
from ..utils.task_manager import set_alert_job

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
    await message.answer(PROJECT_INFO,pagination_keyboard.get_keyboard())
    await state.set_state(CurrencyState.CHOOSE_PROJECT)

@router.message(CurrencyState.CHOOSE_PROJECT, F.text.in_(pull_of_instruments))
async def get_project_info(message: Message, state: FSMContext):
    symbol = message.text
    await message.answer(text='Please wait for a response, we ask for an AI response to be prepared. This may take up to 1 minute.')
    await state.get_data()
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, lambda: asyncio.run(get_project_info_openai(symbol)))
    await message.answer(result)

@router.message(F.text=='Get coin news')
async def get_coin_news(message:Message):
    data = json.loads(storage.get('news'))["news"]
    for new in data:
        answer_text = (f'<b>{new["title"]}</b>\n'
                       f'{new["text"]}\n'
                       f'{new["link"]}\n\n'
                       f'{new["date"]}')
        await message.answer(text=answer_text)


@router.message(F.text=='Set price notification for instrument')
async def set_alert(message:Message, state:FSMContext):
    await message.answer(INSTRUMENTS_LIST,reply_markup=pagination_keyboard.get_keyboard())
    await state.set_state(CurrencyState.SET_ALERT)

@router.message(CurrencyState.SET_ALERT, F.text.in_(pull_of_instruments))
async def alert_set_currency(message:Message, state:FSMContext):
    await message.answer(text='Choose direction up or down.', reply_markup=alet_direction_keyboard)
    await state.update_data(symbol=message.text)
    await state.set_state(CurrencyState.CHOOSE_DIRECTION)

# #@router.message(CurrencyState.SET_ALERT_PRICE)
# #async def alert_set_price(message:Message, state:FSMContext, bot:Bot):
#     #try:
#         price = float(message.text) if "," not in message.text else float(message.text.replace(",","."))
#         set_alert_job(price, chat_id=message.from_user.id)
#         await message.answer('Alert seted')
#         await state.clear()
#     except ValueError:
#         await message.answer("Please try again")

@router.callback_query(F.data.in_(['up','down']))
async def set_alert_price_up(callback:CallbackQuery,state:FSMContext):
    await callback.message.answer(SET_ALERT)
    await callback.answer('set_direction')
    await state.update_data(alert_direction=callback.data)
    await state.set_state(CurrencyState.SET_ALERT_PRICE)



@router.message(CurrencyState.SET_ALERT_PRICE)
async def alert_set_price(message:Message, state:FSMContext, bot:Bot):
    data = await state.get_data()
    symbol = data['symbol']
    price = float(message.text)
    direction = data['alert_direction']
    alert = CoinAlert(chat_id=message.chat.id,tg_bot=bot,symbol=symbol,price=price,direction=direction)
    await alert.run()
    await state.clear()


