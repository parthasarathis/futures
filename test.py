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

# Set up the client
api_key = "FLPeS5t9QAntmcsEtYYv01JBZufM5SQQu751qh0s9rcHwVXZqioztxpMnyVMxvlP"
sec_key = "kP7twDqEL7alJGf4R4uDH6cNsivpscabZ4EEdD9SWJugC7DOJu7YHfcgeP8ngUJw"
partha_account = Client(api_key=api_key, api_secret=sec_key)

coin_price = collections.deque([], maxlen=20)

futures_type = FuturesType.USD_M


def get_tickers(partha_account,yesterday_df,yesterhour_df):
    tickers = partha_account.futures_symbol_ticker()
    df_tickers = pd.DataFrame(tickers)
    df_tickers = df_tickers[df_tickers['symbol'].str.endswith('USDT')]
    df_tickers = df_tickers[~df_tickers['symbol'].str.contains('1000')]
    df_tickers = df_tickers.sort_values('symbol')
    df_tickers = df_tickers.drop('time', axis=1)

    table_data = pd.merge(yesterday_df,yesterhour_df,on='symbol')

    table_data = table_data.rename(columns={'open_price_x': 'Y_D_O_Price', 'close_price_x': 'Y_D_C_Price','open_price_y': 'Y_H_O_Price', 'close_price_y': 'Y_H_C_Price','change_x':'Y_D_Change','change_y':'Y_H_Change'})
    table_data = table_data.drop(['Y_D_O_Price','Y_H_O_Price'],axis=1)
    table_data = pd.merge(table_data,df_tickers,on='symbol')
    table_data =table_data[['symbol','Y_D_Change','Y_D_C_Price','Y_H_Change','Y_H_C_Price','price']]
    table_data['Y_D_C_Price'] = pd.to_numeric(table_data['Y_D_C_Price'], errors='coerce')
    table_data['Y_H_C_Price'] = pd.to_numeric(table_data['Y_H_C_Price'], errors='coerce')
    table_data['price'] = pd.to_numeric(table_data['price'], errors='coerce')
    table_data ['day_change']= (table_data['price'] - table_data['Y_D_C_Price']) /table_data['Y_D_C_Price'] * 100
    table_data ['hour_change']= (table_data['price'] - table_data['Y_H_C_Price']) /table_data['Y_H_C_Price'] * 100
    table_data = table_data.sort_values('day_change',ascending=False)  
    print(tabulate(table_data.head(8), headers='keys', tablefmt='psql'))
    print(tabulate(table_data.tail(8), headers='keys', tablefmt='psql'))
    

def get_data(new_data=False):
    global previous_day_df
    if not path.exists("previous_day_data.csv") or new_data:
        print("previous_data_not_found:")
        tickers = partha_account.futures_ticker()
        column_name_df = pd.DataFrame(tickers)
        column_name_df = column_name_df[column_name_df['symbol'].str.endswith(
            'USDT')]
        busd_list = column_name_df['symbol'].to_list()

        ti_st = int(dt.datetime.now().timestamp())
        time_stamp = int(ti_st - ti_st % 86400)
        start_time = (time_stamp-86400) * 1000
        end_time = (time_stamp*1000 - 1)
        coin_data = collections.deque([], maxlen=int(len(busd_list)/1))

        key_list = ["open_time", "open_price", "high_price", "low_price", "close_price",
                    "volume", "close_time", "asset_volume", "no_of_trades", "TBBAV", "TBQAV", "UNUSED"]
        data = 0
        for coin in busd_list:
            klines = partha_account.futures_historical_klines(
                coin, partha_account.KLINE_INTERVAL_1DAY, start_str=start_time, end_str=end_time)
            if len(klines) > 0:
                res = {key_list[i]: klines[0][i] for i in range(len(key_list))}
            else:
                res = {key_list[i]: "0" for i in range(len(key_list))}
            res['symbol'] = coin
            data += 1
            progress = f"getting data : {data} / {len(busd_list)}"
            print(progress, end="\r")
            coin_data.append(res)
        coin_data_df = pd.DataFrame(coin_data)
        coin_data_df.to_csv("previous_day_data.csv")
        previous_day_df = coin_data_df[['symbol', 'close_price', 'open_price']]
        previous_day_df['change'] = (previous_day_df['close_price'] - previous_day_df['open_price']) / previous_day_df['open_price'] * 100
        previous_day_df = previous_day_df[previous_day_df['symbol'].str.endswith(
            'USDT')]
        previous_day_df = previous_day_df[~previous_day_df['symbol'].str.contains(
            '1000')]
        previous_day_df = previous_day_df.sort_values(
            'change', ascending=False)
        return previous_day_df
    else:
        print("Previous_data_found: Reading from CSV file")
        coin_data_df = pd.read_csv("previous_day_data.csv")
        previous_day_df = coin_data_df[['symbol', 'open_price', 'close_price']]
        previous_day_df['change'] = (previous_day_df['close_price'] - previous_day_df['open_price']) / previous_day_df['open_price'] * 100
        previous_day_df = previous_day_df[previous_day_df['symbol'].str.endswith(
            'USDT')]
        previous_day_df = previous_day_df[~previous_day_df['symbol'].str.contains(
            '1000')]
        previous_day_df = previous_day_df.sort_values(
            'change', ascending=False)
        return previous_day_df

def get_hour_data(new_data=False):
    global previous_hour_df
    if not path.exists("previous_hour_data.csv") or new_data:
        print("previous_hour_data_not_found:")
        tickers = partha_account.futures_ticker()
        column_name_df = pd.DataFrame(tickers)
        column_name_df = column_name_df[column_name_df['symbol'].str.endswith(
            'USDT')]
        busd_list = column_name_df['symbol'].to_list()

        ti_st = int(dt.datetime.now().timestamp())
        time_stamp = int(ti_st - ti_st % 14400)
        start_time = (time_stamp-14400) * 1000
        end_time = (time_stamp*1000 - 1)
        coin_data = collections.deque([], maxlen=int(len(busd_list)/1))

        key_list = ["open_time", "open_price", "high_price", "low_price", "close_price",
                    "volume", "close_time", "asset_volume", "no_of_trades", "TBBAV", "TBQAV", "UNUSED"]
        data = 0
        for coin in busd_list:
            klines = partha_account.futures_historical_klines(
                coin, partha_account.KLINE_INTERVAL_1HOUR, start_str=start_time, end_str=end_time)
            if len(klines) > 0:
                res = {key_list[i]: klines[0][i] for i in range(len(key_list))}
            else:
                res = {key_list[i]: "0" for i in range(len(key_list))}
            res['symbol'] = coin
            data += 1
            progress = f"getting data : {data} / {len(busd_list)}"
            print(progress, end="\r")
            coin_data.append(res)
        coin_data_df = pd.DataFrame(coin_data)
        coin_data_df.to_csv("previous_hour_data.csv")
        previous_hour_df = coin_data_df[['symbol', 'close_price','open_price']]
        previous_hour_df['change'] = (previous_hour_df['close_price'] - previous_hour_df['open_price']) / previous_hour_df['open_price'] * 100
        previous_hour_df = previous_hour_df[previous_hour_df['symbol'].str.endswith(
            'USDT')]
        previous_hour_df = previous_hour_df[~previous_hour_df['symbol'].str.contains(
            '1000')]
        previous_hour_df = previous_hour_df.sort_values(
            'change', ascending=False)
        return previous_hour_df
    else:
        print("Previous_hour_data_found: Reading from CSV file")
        coin_data_df = pd.read_csv("previous_hour_data.csv")
        previous_hour_df = coin_data_df[['symbol', 'open_price', 'close_price']]
        previous_hour_df['change'] = (previous_hour_df['close_price'] - previous_hour_df['open_price']) / previous_hour_df['open_price'] * 100
        previous_hour_df = previous_hour_df[previous_hour_df['symbol'].str.endswith(
            'USDT')]
        previous_hour_df = previous_hour_df[~previous_hour_df['symbol'].str.contains(
            '1000')]
        previous_hour_df = previous_hour_df.sort_values(
            'change', ascending=False)
        return previous_hour_df


print(pyfiglet.figlet_format("Binance Bot"))
previous_day_df = get_data()
previous_hour_df = get_hour_data()

sch.every().day.at("05:30:00").do(get_data, new_data=True)
sch.every().hour.at(":30").do(get_hour_data)
sch.every().minute.at(":05").do(get_tickers, partha_account=partha_account, yesterday_df=previous_day_df,yesterhour_df=previous_hour_df)
sch.every().minute.at(":35").do(get_tickers, partha_account=partha_account, yesterday_df=previous_day_df,yesterhour_df=previous_hour_df)

while True:
    sch.run_pending()
