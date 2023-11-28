import requests
import ccxt
from binance.client import Client
from Config.settings import BINANCE_KEY, BINANCE_SECRET
from Main_bot.utils.forcast import get_binance_signals

#Constants
binance_api_url = "https://api.binance.com/api/v3"
exchange_info = requests.get(f"{binance_api_url}/exchangeInfo").json()

#Creating object Binance API
binance = ccxt.binance({
    'apiKey': BINANCE_KEY,
    'secret': BINANCE_SECRET,
})

#all timeframes form API
timeframe = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']

#getting modified timeframe for text
def modify_timeframe(timeframe):
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
        '1M': '1 month'
    }
    return timeframes.get(timeframe, None)


#Getting of list with USDT pairs
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
    client = Client(BINANCE_KEY, BINANCE_SECRET)
    limit = 1
    klines = client.get_klines(symbol=symbol, interval=timeframe, limit=limit)
    if klines:
        return float(klines[0][4])
    else:
        return None

def get_timeframe_volume(symbol, timeframe):
    client = Client(BINANCE_KEY, BINANCE_SECRET)
    limit = 1
    klines = client.get_klines(symbol=symbol, interval=timeframe, limit=limit)
    if klines:
        return float(klines[0][5])
    else:
        return None

def get_binance_max(symbol, timeframe):
    client = Client(BINANCE_KEY, BINANCE_SECRET)
    limit = 1
    klines = client.get_klines(symbol=symbol, interval=timeframe, limit=limit)
    if klines:
        highs = [str(float(k[2])) for k in klines]
        result_string = ', '.join(highs)
        return result_string
    else:
        return None

def get_binance_min(symbol, timeframe):
    client = Client(BINANCE_KEY, BINANCE_SECRET)
    limit = 1
    klines = client.get_klines(symbol=symbol, interval=timeframe, limit=limit)
    if klines:
        lows = [str(float(k[3])) for k in klines]
        result_string = ', '.join(lows)
        return result_string
    else:
        return None


#Command of getting general information for {symbol} and {timeframe} setted by user
def get_currency_info(symbol,timeframe = '1d'):
    # Creating modified symbol for currencies (examples: modified_symbol = BTC, ETH, XRP, etc.)
    modified_symbol = symbol.replace('USDT', '')
    current_price = get_current_price(symbol, timeframe=timeframe)
    current_volume = get_timeframe_volume(symbol, timeframe=timeframe)
    max_price = get_binance_max(symbol, timeframe=timeframe)
    min_price = get_binance_min(symbol, timeframe=timeframe)
    avg_price_timeframe = round((float(max_price)+float(min_price))/2,2)
    div_absolute = round(avg_price_timeframe - current_price,2)
    div_percentage = round(div_absolute/current_price,3)
    text=    f'Here is the general information from Binance for {modified_symbol} with {modify_timeframe(timeframe)} timeframe:\n'\
              f'Instrument: {modified_symbol}\n'\
              f'Timeframe: {modify_timeframe(timeframe)}\n'\
              f'Current price: {current_price}\n'\
              f'Trading volume of last candle with {modify_timeframe(timeframe)} timeframe: {current_volume} {modified_symbol}\n'\
              f'Maximum price in the last {modify_timeframe(timeframe)}: ${max_price}\n'\
              f'Minimum price in the last {modify_timeframe(timeframe)}: ${min_price}\n'\
               f'Average price in the last {modify_timeframe(timeframe)}: ${avg_price_timeframe}\n'\
               f'Deviation from the average price in the last {modify_timeframe(timeframe)}:\n'\
               f'In absolute terms: ${div_absolute}\n'\
               f'In percentage: {div_percentage}%\n'\
               f'Binance Forecast: {get_binance_signals(symbol)}'
    return text

print(type(get_currency_info("BTCUSDT","1d")))