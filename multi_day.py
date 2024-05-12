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

# Set up the client
api_key = "FLPeS5t9QAntmcsEtYYv01JBZufM5SQQu751qh0s9rcHwVXZqioztxpMnyVMxvlP"
sec_key = "kP7twDqEL7alJGf4R4uDH6cNsivpscabZ4EEdD9SWJugC7DOJu7YHfcgeP8ngUJw"
partha_account = Client(api_key=api_key, api_secret=sec_key)

# Binance API endpoint for futures prices
endpoint = "https://fapi.binance.com/fapi/v1/klines"

# Parameters for the API request

interval = "1W"
limit = 10

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
df_combined = df_combined.sort_values(
    by=df_combined.index[-1], axis=1, ascending=False)
df_combined = df_combined.transpose()

one_positive = df_combined[(
    df_combined.iloc[:, -1:].gt(0).all(axis=1)) & (df_combined.iloc[:, -2].lt(0))]
one_negative = df_combined[(
    df_combined.iloc[:, -1:].lt(0).all(axis=1)) & (df_combined.iloc[:, -2].gt(0))]
two_positive = df_combined[(
    df_combined.iloc[:, -2:].gt(0).all(axis=1)) & (df_combined.iloc[:, -3].lt(0))]
two_negative = df_combined[(
    df_combined.iloc[:, -2:].lt(0).all(axis=1)) & (df_combined.iloc[:, -3].gt(0))]
three_positive = df_combined[(
    df_combined.iloc[:, -3:].gt(0).all(axis=1)) & (df_combined.iloc[:, -4].lt(0))]
three_negative = df_combined[(
    df_combined.iloc[:, -3:].lt(0).all(axis=1)) & (df_combined.iloc[:, -4].gt(0))]
four_positive = df_combined[df_combined.iloc[:, -4:].gt(0).all(axis=1)]
four_negative = df_combined[df_combined.iloc[:, -4:].lt(0).all(axis=1)]


print(pyfiglet.figlet_format("one_positive"))
print(tabulate(one_positive, headers='keys', tablefmt='psql'))
print(pyfiglet.figlet_format("one_negative"))
print(tabulate(one_negative, headers='keys', tablefmt='psql'))
print(pyfiglet.figlet_format("two_positive"))
print(tabulate(two_positive, headers='keys', tablefmt='psql'))
print(pyfiglet.figlet_format("two_negative"))
print(tabulate(two_negative, headers='keys', tablefmt='psql'))
print(pyfiglet.figlet_format("three_positive"))
print(tabulate(three_positive, headers='keys', tablefmt='psql'))
print(pyfiglet.figlet_format("three_negative"))
print(tabulate(three_negative, headers='keys', tablefmt='psql'))
print(pyfiglet.figlet_format("four_positive"))
print(tabulate(four_positive, headers='keys', tablefmt='psql'))
print(pyfiglet.figlet_format("four_negative"))
print(tabulate(four_negative, headers='keys', tablefmt='psql'))

# Print the combined DataFrame with colors
for column in df_combined:
    print(f"{column.split('(')[-1].rstrip(')')} ", end="")
    for value in df_combined[column]:
        if pd.isna(value):
            print("NaN", end=" ")
        elif value >= 0:
            # Green for positive numbers
            print(f"\033[92m{value:+.6f}\033[0m", end=" ")
        else:
            # Red for negative numbers
            print(f"\033[91m{value:+.6f}\033[0m", end=" ")
    print()


# Drop the first empty column
df = four_positive

# Plot each row as a separate line plot
plt.figure(figsize=(12, 6))  # Adjust the figure size if needed
for index, row in df.iterrows():
    plt.plot(row.index, row, marker='o', label=row.name)

# Add labels and title
plt.xlabel('Columns')
plt.ylabel('Values')
plt.title('Line Plot of Rows in DataFrame')

# Add a legend to distinguish between rows
plt.legend()

# Show the plot
plt.show()
