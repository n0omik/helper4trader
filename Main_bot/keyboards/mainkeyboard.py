from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from Main_bot.utils.binance_api import pull_of_instruments

keyboard_main_commands = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text = 'Get general exchange information')],
        [KeyboardButton(text = 'Get general coin information')],
         [KeyboardButton(text = 'Get coin news')],
         [KeyboardButton(text = 'Set price notification for instrument')]
    ])


#getting list of buttons of currency liquidity list
def get_list_of_currency_buttons(pull_of_instruments):
    list_of_currency_buttons = []
    for currency in pull_of_instruments:
        button = KeyboardButton(text=f'{currency}')
        list_of_currency_buttons.append([button])
    return list_of_currency_buttons

keyboard_currency_list = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=
        get_list_of_currency_buttons(pull_of_instruments)
            )

print(get_list_of_currency_buttons(pull_of_instruments))