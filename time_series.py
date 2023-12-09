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
symbol = 'BTCUSDT'

# Function to fetch klines (candlestick) data from Binance API
def get_klines_data(interval='1m', limit=10):
    params = {'symbol': symbol, 'interval': interval, 'limit': limit}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                         'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                                         'taker_buy_quote_asset_volume', 'ignore'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')  # Convert timestamp to datetime format
        df.set_index('timestamp', inplace=True)
        df['close'] = df['close'].astype(float)
        return df
    else:
        print("Failed to fetch klines data. Status Code:", response.status_code)
        return None

# Function for ARIMA forecasting
def arima_forecast(data, p, d, q):
    model = sm.tsa.ARIMA(data, order=(p, d, q))
    model_fit = model.fit()
    forecast= model_fit.forecast(steps=1)
    return forecast[0]

# Main loop for data collection and time series analysis
if __name__ == "__main__":
    # Initialize empty lists to store actual and forecasted BTC prices
    actual_prices = []
    forecasted_prices = []
    forecast_periods = 10  # Number of periods to forecast

    # Create a blank figure and axis for the animation
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('BTC Price (USDT)')
    ax.set_title('Actual vs. Forecasted BTC Price')
    ax.grid(True)

    # Plot initial empty lines for actual and forecasted prices
    actual_line, = ax.plot([], [], label='Actual BTC Price', color='blue')
    forecasted_line, = ax.plot([], [], label='Forecasted BTC Price', color='red')

    # Legend and formatting
    ax.legend()

    # Animation function to update the plot
    def update(frame):
        # Fetch BTC price klines data for the last 10 minutes (adjust the interval and limit as needed)
        df = get_klines_data(interval='1m', limit=10)

        if df is not None and len(df) >= 10:
            # Get the current timestamp for the latest data point
            timestamp = df.index[-1]

            # Fetch the BTC price for the latest data point
            btc_price = df['close'][-1]

            # Perform ARIMA forecasting on the BTC price data
            next_btc_price = arima_forecast(df['close'], p=1, d=1, q=1)

            # Append actual and forecasted prices to the lists
            actual_prices.append(btc_price)
            forecasted_prices.append(next_btc_price)

            # Update the actual and forecasted lines data in the plot
            actual_line.set_data(df.index, actual_prices)
            forecasted_line.set_data(df.index[-1], forecasted_prices[-1])

            # Set the plot limits based on the current data
            ax.set_xlim(df.index[0], df.index[-1])
            ax.set_ylim(min(min(actual_prices), min(forecasted_prices)),
                        max(max(actual_prices), max(forecasted_prices)))

            # Forecast the next 10 values using ARIMA forecast
            future_forecast = []
            for i in range(forecast_periods):
                next_btc_price = arima_forecast(df['close'], p=1, d=1, q=1)
                future_forecast.append(next_btc_price)
                df = pd.concat(pd.Series({'close': next_btc_price}, name=timestamp))
                timestamp += pd.Timedelta(minutes=1)

            print("Forecasted Next 10 Values:", future_forecast)

        return actual_line, forecasted_line

    # Create the animation
    ani = FuncAnimation(fig, update, frames=range(10), interval=60000)  # Update every 60 seconds (1 minute)

    # Show the animation
    plt.show()
