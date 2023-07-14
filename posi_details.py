
from binance.client import Client
from binance.enums import *
import time

# Set up the client
api_key = "FLPeS5t9QAntmcsEtYYv01JBZufM5SQQu751qh0s9rcHwVXZqioztxpMnyVMxvlP"
sec_key = "kP7twDqEL7alJGf4R4uDH6cNsivpscabZ4EEdD9SWJugC7DOJu7YHfcgeP8ngUJw"
partha_account = Client(api_key=api_key, api_secret=sec_key)

futures_type = FuturesType.USD_M


def get_position():
    position = partha_account.futures_position_information()
    for p in position:
        if float(p['positionAmt']) != 0.0:
            pnl = float(p['unRealizedProfit'])
            symbol = p['symbol']
            if pnl >= 0:
                print(f"{symbol } : \033[92m{pnl:+.6f}\033[0m", end=" ")  # Green for positive numbers
            else:
                print(f"{symbol }\033[91m{pnl:+.6f}\033[0m", end=" ")  # Red for negative numbers

while(1):
    print("\033c", end="")
    get_position()
    time.sleep(10)
    