import requests
import pandas as pd
import time
import statsmodels.api as sm
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Replace YOUR_API_KEY and YOUR_SECRET_KEY with your actual Binance API credentials
API_KEY = "FLPeS5t9QAntmcsEtYYv01JBZufM5SQQu751qh0s9rcHwVXZqioztxpMnyVMxvlP"
SECRET_KEY = "kP7twDqEL7alJGf4R4uDH6cNsivpscabZ4EEdD9SWJugC7DOJu7YHfcgeP8ngUJw"

# Binance API endpoint for klines (candlestick) data for BTC/USDT perpetual futures
url = 'https://fapi.binance.com/fapi/v1/klines'

# Symbol for BTC/USDT perpetual futures
symbol = 'ADAUSDT'

# Function to fetch klines (candlestick) data from Binance API


def get_klines_data(interval='15m', limit=1000):
    params = {'symbol': symbol, 'interval': interval, 'limit': limit}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                         'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                                         'taker_buy_quote_asset_volume', 'ignore'])
        # Convert timestamp to datetime format
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
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
    data = get_klines_data(interval='15m', limit=100)
    # Plotting high and low prices
    plt.plot(data['high'], label='High')
    plt.plot(data['low'], label='Low')

    # plt.bar(data.index, data['volume'], label='Volume')

    plt.legend()
    plt.xticks(rotation=45)  # Rotate x-axis labels by 45 degrees
    plt.show()
