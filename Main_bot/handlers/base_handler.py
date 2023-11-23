from aiogram.types import Message
from aiogram import types, Router, F
from aiogram.filters import Command, CommandStart
from ..Text import START_MESSAGE, INSTRUMENTS_LIST
from Main_bot.keyboards.mainkeyboard import keyboard_main_commands,keyboard_currency_list
# from Main_bot.utils.binance_api import pull_of_instruments


router = Router()

# pull_of_instruments()


@router.message(Command('start'))
async def start_handler(message:Message):
    await message.answer(START_MESSAGE,reply_markup=keyboard_main_commands)

@router.message(F.text=='Get general exchange information')
async def get_exchange_info(message:Message):
    await message.answer(INSTRUMENTS_LIST,reply_markup=keyboard_currency_list)

#print(pull_of_instruments)


