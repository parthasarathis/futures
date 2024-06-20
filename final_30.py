
from binance.client import Client
from binance.enums import FuturesType
import time
import datetime as dt
import pandas as pd
import schedule as sch
from tabulate import tabulate
import pyfiglet
from os import path
import collections
import numpy as np
import streamlit as st
import requests
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Binance API endpoint for futures prices
endpoint = "https://fapi.binance.com/fapi/v1/klines"

# Set up the client
api_key = "FLPeS5t9QAntmcsEtYYv01JBZufM5SQQu751qh0s9rcHwVXZqioztxpMnyVMxvlP"
sec_key = "kP7twDqEL7alJGf4R4uDH6cNsivpscabZ4EEdD9SWJugC7DOJu7YHfcgeP8ngUJw"
partha_account = Client(api_key=api_key, api_secret=sec_key)

coin_price = collections.deque([], maxlen=20)

futures_type = FuturesType.USD_M

st.set_page_config(layout='wide')
pd.set_option('display.max_rows', 20)


print(partha_account.futures_symbol_ticker())
