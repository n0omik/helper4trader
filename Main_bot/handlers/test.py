import asyncio
import json

import websockets

BINANCE_KEY = 'gpmetY3J1WFMidb6QgqwjqWSCoNHfjWySLCwcxikhOPvV71YaSz9ewmaybkEirWp'
BINANCE_SECRET = 'LWm12UY1f02z8ozqBNJzoLWTLgBEFPFCcTKpf6T3FnwEMuDCjcKpEY21YbAzx1YU'
alerts = []


def send_message(text):
    pass


async def on_open(ws):
    sub_msg = {
        "method": "SUBSCRIBE",
        "params": [
            "!miniTicker@arr",
        ],
        "id": 1,
    }

    await ws.send(json.dumps(sub_msg))
    print('open connection')


async def alert_down(symbol, price, data):
    # print(data)
    try:
        for x in data:
            if x['s'] == 'BTCUSDT':
                print('BTCUSDT', x['c'])
            if x['s'] == symbol and float(x['c']) <= price:
                print(f'--{x["s"]} {x["c"]}--')
                send_message(f'{x["s"]} {x["c"]}')
    except:
        pass


async def on_message(ws, message):
    data = json.loads(message)
    await alert_down('BTCUSDT', 44050, data)


async def main():
    url = 'wss://stream.binance.com/ws'

    async with websockets.connect(url) as ws:
        await on_open(ws)

        while True:
            response = await ws.recv()
            await on_message(ws, response)


if __name__ == "__main__":
    asyncio.run(main())
