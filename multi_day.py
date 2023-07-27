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
import requests

# Set up the client
api_key = "FLPeS5t9QAntmcsEtYYv01JBZufM5SQQu751qh0s9rcHwVXZqioztxpMnyVMxvlP"
sec_key = "kP7twDqEL7alJGf4R4uDH6cNsivpscabZ4EEdD9SWJugC7DOJu7YHfcgeP8ngUJw"
partha_account = Client(api_key=api_key, api_secret=sec_key)

# Binance API endpoint for futures prices
endpoint = "https://fapi.binance.com/fapi/v1/klines"

# Parameters for the API request

interval = "1d"
limit = 15

# Create an empty DataFrame
df_combined = pd.DataFrame()

if not path.exists("multiday_data.csv"):
    print("previous_data_not_found:")
    tickers = partha_account.futures_ticker()
    column_name_df = pd.DataFrame(tickers)
    column_name_df = column_name_df[column_name_df['symbol'].str.endswith(
        'USDT')]
    symbols = column_name_df['symbol'].to_list()
    data1 = 0   

    for symbol in symbols:
        # Construct the API request URL
        params = {"symbol": symbol, "interval": interval, "limit": limit}
        response = requests.get(endpoint, params=params)
        data = response.json()
        data1 += 1
        progress = f"getting data : {data1} / {len(symbols)}"
        print(progress, end="\r")

        # Convert the data to a DataFrame
        df = pd.DataFrame(data, columns=["Open Time", "Open", "High", "Low", "Close", "Volume", "Close Time",
                                        "Quote Asset Volume", "Number of Trades", "Taker Buy Base Asset Volume",
                                        "Taker Buy Quote Asset Volume", "Ignore"])
        df["Open Time"] = pd.to_datetime(df["Open Time"], unit="ms").dt.date
        df["Close"] = pd.to_numeric(df["Close"])

        # Calculate rate of change for each day
        column_name = f"{symbol}"
        df[column_name] = df['Close'].pct_change() * 100

        # Append to the combined DataFrame
        df_combined = pd.concat([df_combined, df[[column_name]]], axis=1)
    
    df_combined.to_csv("multiday_data.csv")
    time.sleep(1)

else:
    print("previous_data_found:")
    df_combined = pd.read_csv("multiday_data.csv")
   



# Rename the column header to "Open Time"
# df_combined.rename(columns={"Open Time": "Open Time"}, inplace=True)

# Sort the DataFrame by the last column in ascending order
df_combined = df_combined.sort_values(by=df_combined.index[-1], axis=1,ascending=False)

# Print the combined DataFrame with colors
for column in df_combined:
    print(f"{column.split('(')[-1].rstrip(')')} ", end="")
    for value in df_combined[column]:
        if pd.isna(value):
            print("NaN", end=" ")
        elif value >= 0:
            print(f"\033[92m{value:+.6f}\033[0m", end=" ")  # Green for positive numbers
        else:
            print(f"\033[91m{value:+.6f}\033[0m", end=" ")  # Red for negative numbers
    print()
