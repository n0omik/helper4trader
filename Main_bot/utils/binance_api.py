import requests
import ccxt
import json
import certifi
import ssl
from binance.client import Client
from Config.settings import Config
from Main_bot.utils.forcast import get_binance_signals
import websockets
from aiogram import Bot
import asyncio

#certifs = certifi.where('/Users/pasharybalchenko/Python_projects/Telegram_bot_main/venv/lib/python3.11/site-packages/certifi')
#ssl_context = ssl.create_default_context(cafile=certifi)

#Constants
binance_api_url = "https://api.binance.com/api/v3"
exchange_info = requests.get(f"{binance_api_url}/exchangeInfo").json()

#Creating object Binance API
binance = ccxt.binance({
    'apiKey': Config.BINANCE_KEY,
    'secret': Config.BINANCE_SECRET,
})

#all timeframes form API
timeframes = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']

#getting modified timeframe for text
# def modify_timeframe(timeframe):
#     timeframes = {
#         '1m': '1 minute',
#         '3m': '3 minutes',
#         '5m': '5 minutes',
#         '15m': '15 minutes',
#         '30m': '30 minutes',
#         '1h': '1 hour',
#         '2h': '2 hours',
#         '4h': '4 hours',
#         '6h': '6 hours',
#         '8h': '8 hours',
#         '12h': '12 hours',
#         '1d': '24 hours',
#         '3d': '3 days',
#         '1w': '1 week',
#         '1M': '1 month'
#     }
#     return timeframes.get(timeframe, None)


timeframes = {
        '1m': '1 minute',
        '3m': '3 minutes',
        '5m': '5 minutes',
        '15m': '15 minutes',
        '30m': '30 minutes',
        '1h': '1 hour',
        '2h': '2 hours',
        '4h': '4 hours',
        '6h': '6 hours',
        '8h': '8 hours',
        '12h': '12 hours',
        '1d': '24 hours',
        '3d': '3 days',
        '1w': '1 week',
        '1M': '1 month'}



timeframe_reterned = {
        '1 minute':'1m',
        '3 minutes':"3m",
        '5 minutes':"5m",
        '15 minutes':"15m",
        '30 minutes':"30m",
        '1 hour':"1h",
        '2 hours':"2h",
        '4 hours':"4h",
        '6 hours':"6h",
        '8 hours':"8h",
        '12 hours':"12h",
        '24 hours':"1d",
        '3 days':"3d",
        '1 week':"1w",
        '1 month':"1M"}


class Klines:
    def __init__(self,data):
        self.open_time = data[0][0]
        self.open_price = data[0][1]
        self.high_price = data[0][2]
        self.low_price = data[0][3]
        self.close_price = data[0][4]
        self.volume = data[0][5]
        self._data = data
class BinanceApi:
    liquidity_volume = Config.LIQUIDITY_VOLUME
    timeframes = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']
    timeframes = {
        '1m': '1 minute',
        '3m': '3 minutes',
        '5m': '5 minutes',
        '15m': '15 minutes',
        '30m': '30 minutes',
        '1h': '1 hour',
        '2h': '2 hours',
        '4h': '4 hours',
        '6h': '6 hours',
        '8h': '8 hours',
        '12h': '12 hours',
        '1d': '24 hours',
        '3d': '3 days',
        '1w': '1 week',
        '1M': '1 month'}

    timeframe_reterned = {
        '1 minute': '1m',
        '3 minutes': "3m",
        '5 minutes': "5m",
        '15 minutes': "15m",
        '30 minutes': "30m",
        '1 hour': "1h",
        '2 hours': "2h",
        '4 hours': "4h",
        '6 hours': "6h",
        '8 hours': "8h",
        '12 hours': "12h",
        '24 hours': "1d",
        '3 days': "3d",
        '1 week': "1w",
        '1 month': "1M"}

    def __init__(self,symbol,interval, limit=1):
        self._key = Config.BINANCE_KEY
        self._secret_key = Config.BINANCE_SECRET
        self.client = Client(self._key, self._secret_key)
        self.limit = limit
        self.symbol = symbol
        self.interval = interval
        self.klines = Klines(self.client.get_klines(symbol=self.symbol,interval =self.interval,limit=self.limit))


    def get_current_price(self):
        return self.klines.close_price

    def get_timeframe_volume(self):
        return self.klines.volume

    def get_min_price(self):
        lows = [k[3]for k in self.klines._data]
        return ', '.join(lows)

    def get_max_price(self):
        maximum = [k[2] for k in self.klines._data]
        return ', '.join(maximum)

    def get_usdt_pairs(self):
        data = self.client.get_all_tickers()
        usdt_pairs = []
        for tikers in data:
            if 'USDT' in tikers.get("symbol"):
                usdt_pairs.append(tikers.get('symbol'))
        return usdt_pairs

    def get_liquidity_instruments(self):
        usd_pairs = self.get_usdt_pairs()
        liquidity_instruments = []
        data = self.client.get_ticker()
        for symbol in data:
            if float(symbol.get('quoteVolume')) > self.liquidity_volume and symbol.get('symbol') in usd_pairs:
                liquidity_instruments.append(symbol.get('symbol'))
        return liquidity_instruments



def get_usdt_pairs():
    usdt_pairs = []
    url = f'{binance_api_url}/exchangeInfo'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for symbol_info in data['symbols']:
            symbol = symbol_info['symbol']
            if 'USDT' in symbol:
                usdt_pairs.append(symbol)
        return usdt_pairs
    else:
        print("Error with getting info")


#getting liquid instruments with symbols and 24h trading volume
def get_liquidity_instruments(symbols, volume):
    liquid_pairs = []
    url = f"{binance_api_url}/ticker/24hr"
    response = requests.get(url)
    ticker_info = response.json()
    for item in ticker_info:
        symbol = item['symbol']
        daily_volume = float(item['quoteVolume'])
        if daily_volume > volume and any(symbol in pair for pair in symbols):
            liquid_pairs.append(symbol)
    return liquid_pairs

#Creting pull of liquid instruments with volume of 1000000 usd per 24h
pull_of_instruments = get_liquidity_instruments(get_usdt_pairs(),10000000)


def get_current_price(symbol, timeframe='1m'):
    client = Client(Config.BINANCE_KEY, Config.BINANCE_SECRET)
    limit = 1
    klines = client.get_klines(symbol=symbol, interval=timeframe, limit=limit)
    if klines:
        return float(klines[0][4])
    else:
        return None

def get_timeframe_volume(symbol, timeframe):
    client = Client(Config.BINANCE_KEY, Config.BINANCE_SECRET)
    limit = 1
    klines = client.get_klines(symbol=symbol, interval=timeframe, limit=limit)
    if klines:
        return float(klines[0][5])
    else:
        return None

def get_binance_max(symbol, timeframe):
    client = Client(Config.BINANCE_KEY, Config.BINANCE_SECRET)
    limit = 1
    klines = client.get_klines(symbol=symbol, interval=timeframe, limit=limit)
    if klines:
        highs = [str(float(k[2])) for k in klines]
        result_string = ', '.join(highs)
        return result_string
    else:
        return None

def get_binance_min(symbol, timeframe):
    client = Client(Config.BINANCE_KEY, Config.BINANCE_SECRET)
    limit = 1
    klines = client.get_klines(symbol=symbol, interval=timeframe, limit=limit)
    if klines:
        lows = [str(float(k[3])) for k in klines]
        result_string = ', '.join(lows)
        return result_string
    else:
        return None


#Command of getting general information for {symbol} and {timeframe} setted by user
def get_currency_info(symbol,timeframe):
    # Creating modified symbol for currencies (examples: modified_symbol = BTC, ETH, XRP, etc.)
    modified_symbol = symbol.replace('USDT', '')
    current_price = get_current_price(symbol, timeframe=timeframe)
    current_volume = get_timeframe_volume(symbol, timeframe=timeframe)
    max_price = get_binance_max(symbol, timeframe=timeframe)
    min_price = get_binance_min(symbol, timeframe=timeframe)
    avg_price_timeframe = round((float(max_price)+float(min_price))/2,2)
    div_absolute = round(avg_price_timeframe - current_price,2)
    div_percentage = round(div_absolute/current_price,3)
    text=    f'Here is the general information from Binance for {modified_symbol} with {timeframes.get(timeframe)} timeframe:\n'\
              f'Instrument: {modified_symbol}\n'\
              f'Timeframe: {timeframes.get(timeframe)}\n'\
              f'Current price: {current_price}\n'\
              f'Trading volume of last candle with {timeframes.get(timeframe)} timeframe: {current_volume} {modified_symbol}\n'\
              f'Maximum price in the last {timeframes.get(timeframe)}: ${max_price}\n'\
              f'Minimum price in the last {timeframes.get(timeframe)}: ${min_price}\n'\
               f'Average price in the last {timeframes.get(timeframe)}: ${avg_price_timeframe}\n'\
               f'Deviation from the average price in the last {timeframes.get(timeframe)}:\n'\
               f'In absolute terms: ${div_absolute}\n'\
               f'In percentage: {div_percentage}%\n'\
               f'n0omik Forecast: {get_binance_signals(symbol)}'
    return text


class CoinAlert:
    url = 'wss://stream.binance.com/ws'

    def __init__(self, chat_id, tg_bot, symbol, price,direction):
        self.symbol = symbol
        self.price = price
        self.tg_bot = tg_bot
        self.chat_id = chat_id
        self.direction = direction

    async def send_message(self, text):
        # Реализация метода send_message
        pass

    async def on_open(self, ws):
        sub_msg = {
            "method": "SUBSCRIBE",
            "params": [
                "!miniTicker@arr",
            ],
            "id": 1,
        }

        await ws.send(json.dumps(sub_msg))
    print('open connection')
    async def alert_down(self, data, ws):
            try:
                for x in data:
                    if x['s'] == 'BTCUSDT':
                        print('BTCUSDT', x['c'])
                    if x['s'] == self.symbol and float(x['c']) <= self.price:
                        print(f'--{x["s"]} {x["c"]}--')
                        await self.tg_bot.send_message(chat_id = self.chat_id, text = f"Price of {self.symbol} riched your alert price and now is {x['c']}.")
                        await ws.close()
            except Exception as e:
                print(f"An error occurred: {e}")

    async def alert_up(self, data, ws):
            try:
                for x in data:
                    if x['s'] == 'BTCUSDT':
                        print('BTCUSDT', x['c'])
                    if x['s'] == self.symbol and float(x['c']) >= self.price:
                        print(f'--{x["s"]} {x["c"]}--')
                        await self.tg_bot.send_message(chat_id = self.chat_id, text = f"Price of {self.symbol} riched your alert price and now is {x['c']}.")
                        await ws.close()
            except Exception as e:
                print(f"An error occurred: {e}")


    async def on_message(self, message, ws):
            data = json.loads(message)
            if self.direction == 'down':
                await self.alert_down(data,ws)
            elif self.direction == 'up':
                await self.alert_up(data,ws)

    async def run(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname=False
        ssl_context.verify_mode=ssl.CERT_NONE
        async with websockets.connect(self.url, ssl=ssl_context) as ws:
            await self.on_open(ws)

            while True:
                response = await ws.recv()
                await self.on_message(response,ws)

