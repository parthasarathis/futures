import requests
import pandas as pd
import time
import statsmodels.api as sm
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from scipy.signal import argrelextrema
import mplfinance as mpf


Time_frame = '15m'
limit = 100


# Replace YOUR_API_KEY and YOUR_SECRET_KEY with your actual Binance API credentials
API_KEY = "FLPeS5t9QAntmcsEtYYv01JBZufM5SQQu751qh0s9rcHwVXZqioztxpMnyVMxvlP"
SECRET_KEY = "kP7twDqEL7alJGf4R4uDH6cNsivpscabZ4EEdD9SWJugC7DOJu7YHfcgeP8ngUJw"

# Binance API endpoint for klines (candlestick) data for BTC/USDT perpetual futures
url = 'https://fapi.binance.com/fapi/v1/klines'

# Symbol for BTC/USDT perpetual futures
symbol = 'ADAUSDT'

# Function to fetch klines (candlestick) data from Binance API


def get_klines_data(interval='1h', limit=1000):
    params = {'symbol': symbol, 'interval': interval, 'limit': limit}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                         'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                                         'taker_buy_quote_asset_volume', 'ignore'])
        # Convert timestamp to datetime format
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['close'] = df['close'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df['open'] = df['open'].astype(float)
        return df
    else:
        print("Failed to fetch klines data. Status Code:", response.status_code)
        return None

# Function for ARIMA forecasting


# Main loop for data collection and time series analysis
if __name__ == "__main__":
    # Initialize empty lists to store actual and forecasted BTC prices
    data = get_klines_data(interval=Time_frame, limit=limit)

    # Convert 'timestamp' column to datetime and set as index
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    # print(data['timestamp'])
    data.set_index('timestamp', inplace=True)

    # Find local maxima
    local_max = argrelextrema(np.array(data['high']), np.greater)[0]
    local_min = argrelextrema(np.array(data['low']), np.less)[0]

    local_extrema = np.sort(np.concatenate((local_max, local_min))).tolist()

    # Create a new figure and an axes
    fig, ax = plt.subplots()

    # Plotting high and low prices
    ax.plot(data['high'], label='High')
    ax.plot(data['low'], label='Low')

    local_max_df = pd.DataFrame({
        'local_max': data['high'].iloc[local_max]
    })  # Create a DataFrame for local maxima

    # print(local_max_df)

    local_min_df = pd.DataFrame({
        'local_min': data['low'].iloc[local_min]
    })  # Create a DataFrame for local minima

    # print(local_min_df)
    # local_extrema_df = pd.concat(
    # [local_max_df, local_min_df]).sort_values('timestamp')

    local_extrema_df = pd.merge(
        local_max_df, local_min_df, on='timestamp', how='outer', sort=True,)

    # local_extrema_df.fillna(0, inplace=True)

    local_extrema_df['local_extrema'] = local_extrema_df['local_max'] + \
        local_extrema_df['local_min']

    print(local_extrema_df)

    # plt.plot(local_extrema_df.index, local_extrema_df['local_extrema'])
    plt.xlabel('Timestamp')
    plt.ylabel('Local Extrema')
    plt.title('Timestamp vs Local Extrema')

    ax.scatter(data.index[local_max],
               data['high'].iloc[local_max], color='r', label='local max')
    ax.scatter(data.index[local_min],
               data['low'].iloc[local_min], color='g', label='local min')

    ax.legend()
    plt.xticks(rotation=45)  # Rotate x-axis labels by 45 degrees

    # Plot candlestick chart
    # mpf.plot(data, type='candle', ax=ax)
    plt.show()
