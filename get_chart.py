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
import numpy as np
import matplotlib.pyplot as plt
import requests
import mplfinance as mpf
import matplotlib.dates as mdates  # Add this line
import matplotlib.ticker as mticker  # Add this line

# Set up the client
api_key = "FLPeS5t9QAntmcsEtYYv01JBZufM5SQQu751qh0s9rcHwVXZqioztxpMnyVMxvlP"
sec_key = "kP7twDqEL7alJGf4R4uDH6cNsivpscabZ4EEdD9SWJugC7DOJu7YHfcgeP8ngUJw"
partha_account = Client(api_key=api_key, api_secret=sec_key)

# Binance API endpoint for futures prices
endpoint = "https://fapi.binance.com/fapi/v1/klines"


# Define the symbol and intervals
symbols = ["USTCUSDT"]
intervals = ["15m", "1h", "4h", "1d"]

# Set the start and end time for the chartt
start_time = int(time.time() * 1000) - 24 * 60 * 60 * 1000  # 24 hours ago
end_time = int(time.time() * 1000)  # current time


# Create subplots
fig, axs = plt.subplots(len(intervals), 1, figsize=(10, 10), sharex=True)

# Iterate over symbols and intervals
for i, symbol in enumerate(symbols):
    for j, interval in enumerate(intervals):
        # Get the candlestick data
        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": start_time,
            "endTime": end_time,
            "limit": 1000  # maximum number of data points to retrieve
        }
        response = requests.get(endpoint, params=params)
        data = response.json()

        # Convert the data into a pandas DataFrame
        df = pd.DataFrame(data, columns=["Open time", "Open", "High", "Low", "Close", "Volume", "Close time",
                                         "Quote asset volume", "Number of trades", "Taker buy base asset volume",
                                         "Taker buy quote asset volume", "Ignore"])
        df["Open"] = df["Open"].astype(float)
        df["High"] = df["High"].astype(float)
        df["Low"] = df["Low"].astype(float)
        df["Close"] = df["Close"].astype(float)
        df["Volume"] = df["Volume"].astype(float)
        df["Open time"] = pd.to_datetime(df["Open time"], unit="ms")
        df.set_index("Open time", inplace=True)

        # Plot the candlestick chart
        ax = axs[j]
        mpf.plot(df, type='candle', style='charles',
                 title=f"{symbol} {interval} Candlestick Chart",
                 ylabel='Price',
                 mav=(3, 6, 9),
                 ax=ax)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
        ax.xaxis.set_major_locator(mticker.MaxNLocator(10))
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        ax.set_title(f"{symbol} {interval} Candlestick Chart")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.grid(True)

        # Adjust the layout and display the chart
        plt.tight_layout()
        plt.show()
