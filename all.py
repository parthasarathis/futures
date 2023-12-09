import pandas as pd
import matplotlib.pyplot as plt
from binance.client import Client
from datetime import datetime

# Replace 'YOUR_API_KEY' and 'YOUR_SECRET_KEY' with your Binance API credentials
api_key = "FLPeS5t9QAntmcsEtYYv01JBZufM5SQQu751qh0s9rcHwVXZqioztxpMnyVMxvlP"
sec_key = "kP7twDqEL7alJGf4R4uDH6cNsivpscabZ4EEdD9SWJugC7DOJu7YHfcgeP8ngUJw"

client = Client(api_key, sec_key)

def convert_unix_to_human_time(unix_time):
    return datetime.fromtimestamp(unix_time / 1000.0).strftime('%Y-%m-%d %H:%M:%S')

def fetch_binance_data(symbol, interval, limit):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['timestamp'] = df['timestamp'].apply(lambda x: convert_unix_to_human_time(x))
    df['close'] = df['close'].astype(float)
    df['open'] = df['open'].astype(float)
    return df

sym = 'LINKUSDT'

fifteen_minute = fetch_binance_data(symbol=sym, interval=Client.KLINE_INTERVAL_1MINUTE, limit=768)

# Fetch data for the last 5 days (5 days * 24 hours/day = 120 hours)
one_hour = fetch_binance_data(symbol=sym, interval=Client.KLINE_INTERVAL_15MINUTE, limit=192)

# Fetch data for the last 30 4-hour periods (30 periods * 4 hours/period = 120 hours)
four_hour = fetch_binance_data(symbol=sym, interval=Client.KLINE_INTERVAL_1HOUR, limit=48)

day_data = fetch_binance_data(symbol=sym, interval=Client.KLINE_INTERVAL_4HOUR, limit=12)

# Combine the datasets


# Plot the combined dataset
plt.figure(figsize=(12, 6))
#plt.plot(one_hour['timestamp'], one_hour['close'],one_hour['open'], label='1 hour')
plt.plot(four_hour['timestamp'], four_hour['close'], label='4close')
plt.plot(four_hour['timestamp'],four_hour['open'], label='open')
plt.plot(day_data['timestamp'], day_data['close'],label='1 day')
plt.plot(day_data['timestamp'], day_data['open'],label='1 day')
plt.xlabel('Time')
plt.ylabel('Close Price')
plt.title(sym)
plt.grid(True)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
