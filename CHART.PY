
import argparse
import requests
import mplfinance as mpf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget
import pandas as pd

# Binance API endpoint
BASE_URL = 'https://fapi.binance.com'

def get_candlestick_data(symbol, interval, limit):
    # API endpoint for fetching candlestick data
    url = f'{BASE_URL}/fapi/v1/klines'

    # Parameters for the request
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }

    # Send GET request to the Binance API
    response = requests.get(url, params=params)
    data = response.json()

    return data

def plot_chart(data, interval, figure):
    # Extract relevant data from the candlestick data
    timestamps = [candle[0] for candle in data]
    opens = [float(candle[1]) for candle in data]
    highs = [float(candle[2]) for candle in data]
    lows = [float(candle[3]) for candle in data]
    closes = [float(candle[4]) for candle in data]
    volumes = [float(candle[5]) for candle in data]

    # Construct a DataFrame from the extracted data
    df = pd.DataFrame({
        'Open': opens,
        'High': highs,
        'Low': lows,
        'Close': closes,
        'Volume': volumes
    }, index=pd.to_datetime(timestamps, unit='ms'))

    # Plot the candlestick chart
    axis = figure.add_subplot(111)
    mpf.plot(df, ax=axis, type='candle', style='binance', ylabel='Price')
    axis.set_title(interval + ' Chart')

# Main program
if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Binance Futures Coin Candlestick Charts')
    parser.add_argument('symbol', type=str, help='Symbol of the futures coin')
    args = parser.parse_args()

    symbol = args.symbol  # Symbol of the futures coin
    limit = 1000  # Number of candles to retrieve (adjust as needed)

    # Get 1-minute chart
    minute_data = get_candlestick_data(symbol, '1m', limit)

    # Get 15-minute chart
    fifteen_minute_data = get_candlestick_data(symbol, '15m', limit)

    # Get 1-hour chart
    hour_data = get_candlestick_data(symbol, '1h', limit)

    # Get 1-day chart
    day_data = get_candlestick_data(symbol, '1d', limit)

    # Create the main application
    app = QApplication([])

    # Create the main window
    main_window = QMainWindow()
    main_window.setWindowTitle('Futures Coin Candlestick Charts')

    # Create a tab widget to hold the charts
    tab_widget = QTabWidget()

    # Create tabs for each interval
    tab1 = QWidget()
    tab2 = QWidget()
    tab3 = QWidget()
    tab4 = QWidget()

    # Create a vertical layout for each tab
    layout1 = QVBoxLayout(tab1)
    layout2 = QVBoxLayout(tab2)
    layout3 = QVBoxLayout(tab3)
    layout4 = QVBoxLayout(tab4)

    # Create a figure and canvas for each tab
    figure1 = plt.Figure()
    canvas1 = FigureCanvas(figure1)
    layout1.addWidget(canvas1)

    figure2 = plt.Figure()
    canvas2 = FigureCanvas(figure2)
    layout2.addWidget(canvas2)

    figure3 = plt.Figure()
    canvas3 = FigureCanvas(figure3)
    layout3.addWidget(canvas3)

    figure4 = plt.Figure()
    canvas4 = FigureCanvas(figure4)
    layout4.addWidget(canvas4)

    # Plot 1-minute chart
    plot_chart(minute_data, '1-minute', figure1)

    # Plot 15-minute chart
    plot_chart(fifteen_minute_data, '15-minute', figure2)

    # Plot 1-hour chart
    plot_chart(hour_data, '1-hour', figure3)

    # Plot 1-day chart
    plot_chart(day_data, '1-day', figure4)

    # Add tabs to the tab widget
    tab_widget.addTab(tab1, '1-minute')
    tab_widget.addTab(tab2, '15-minute')
    tab_widget.addTab(tab3, '1-hour')
    tab_widget.addTab(tab4, '1-day')

    # Set the tab widget as the central widget of the main window
    main_window.setCentralWidget(tab_widget)

    # Show the main window
    main_window.show()

    # Run the application event loop
    app.exec()
