from binance.client import Client
import os
from binance.enums import FuturesType
import time
import datetime as dt
import pandas as pd
import schedule as sch
from tabulate import tabulate
import pyfiglet
from os import path
import collections
from pprint import pprint

# Set up the client
api_key = "FLPeS5t9QAntmcsEtYYv01JBZufM5SQQu751qh0s9rcHwVXZqioztxpMnyVMxvlP"
sec_key = "kP7twDqEL7alJGf4R4uDH6cNsivpscabZ4EEdD9SWJugC7DOJu7YHfcgeP8ngUJw"
partha_account = Client(api_key=api_key, api_secret=sec_key)

coin_price = collections.deque([], maxlen=20)

futures_type = FuturesType.USD_M

key_list = ["open_time", "open_price", "high_price", "low_price", "close_price",
            "volume", "close_time", "asset_volume", "no_of_trades", "TBBAV", "TBQAV", "UNUSED"]
data = 0
klines = partha_account.futures_historical_klines(
    'ADAUSDT', partha_account.KLINE_INTERVAL_15MINUTE, "1 hour ago UTC")


data = dict(zip(key_list, klines))

pprint(data)
