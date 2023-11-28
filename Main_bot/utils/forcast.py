from binance.client import Client
import numpy as np
from Config.settings import BINANCE_KEY, BINANCE_SECRET

client = Client(BINANCE_KEY, BINANCE_SECRET)


def get_binance_signals(symbol):
    interval = '1d'
    limit = 2000
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    close_prices = np.array([float(kline[4]) for kline in klines])
    ma50 = np.mean(close_prices[-50:])
    ma200 = np.mean(close_prices[-200:])
    deviation = ((ma50 - ma200) / ma200) * 100
    max_deviation = np.max(np.abs(np.convolve(close_prices[-50:], np.ones(200) / 200, mode='valid') - ma200) / ma200 * 100)
    if deviation > 0:
        if deviation > 0.5 * max_deviation:
            signal = 'Strong Buy'
        elif deviation > 0.05 * max_deviation:
            signal = 'Buy'
        else:
            signal = 'Neutral'
    else:
        if abs(deviation) > 0.5 * max_deviation:
            signal = 'Strong Sell'
        elif abs(deviation) > 0.05 * max_deviation:
            signal = 'Sell'
        else:
            signal = 'Neutral'
    return signal

# Function check
#symbol = 'SOLUSDT'
#interval = '1d'

#print(f"Текущий сигнал для {symbol}: {get_binance_signals(symbol)}")