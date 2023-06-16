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

# Set up the client
api_key = "FLPeS5t9QAntmcsEtYYv01JBZufM5SQQu751qh0s9rcHwVXZqioztxpMnyVMxvlP"
sec_key = "kP7twDqEL7alJGf4R4uDH6cNsivpscabZ4EEdD9SWJugC7DOJu7YHfcgeP8ngUJw"
partha_account = Client(api_key=api_key, api_secret=sec_key)

coin_price = collections.deque([], maxlen=20)

futures_type = FuturesType.USD_M


 # write comments for below function
def get_tickers(partha_account,yesterday_df,yesterhour_df):
    tickers = partha_account.futures_symbol_ticker()
    df_tickers = pd.DataFrame(tickers)
    df_tickers = df_tickers[df_tickers['symbol'].str.endswith('USDT')]
    df_tickers = df_tickers[~df_tickers['symbol'].str.contains('1000')]
    df_tickers = df_tickers.sort_values('symbol')
    df_tickers = df_tickers.drop('time', axis=1)

    table_data = pd.merge(yesterday_df,yesterhour_df,on='symbol')
    w_table_data = table_data
    #print(w_table_data.columns)
    

    table_data = table_data.rename(columns={'open_price_x': 'D_OPEN', 'high_price_x': 'D_HIGH', 'low_price_x': 'D_LOW','open_price_y': 'H_OPEN', 'high_price_y': 'H_HIGH', 'low_price_y': 'H_LOW','max_change_d': 'D_MAX','min_change_d': 'D_MIN','max_change_h': 'H_MAX','min_change_h': 'H_MIN'})
    # table_data = table_data.drop(['Y_D_O_Price','Y_H_O_Price'],axis=1)
    table_data = pd.merge(table_data,df_tickers,on='symbol')
    table_data['price'] = table_data['price'].astype(float)
    # print(table_data)

    table_data['D_HIGH']=np.maximum(table_data['D_HIGH'],table_data['price'])
    table_data['D_LOW']=np.minimum(table_data['D_LOW'],table_data['price'])
    table_data['H_HIGH']=np.maximum(table_data['H_HIGH'],table_data['price'])
    table_data['H_LOW']=np.minimum(table_data['H_LOW'],table_data['price'])
    table_data['D_MAX'] = (table_data['D_HIGH'] - table_data['D_OPEN'])/table_data['D_OPEN'] * 100
    table_data['D_MIN'] = (table_data['D_LOW'] - table_data['D_OPEN'])/table_data['D_OPEN'] * 100 
    table_data['H_MAX'] = (table_data['H_HIGH'] - table_data['H_OPEN'])/table_data['H_OPEN'] * 100
    table_data['H_MIN'] = (table_data['H_LOW'] - table_data['H_OPEN'])/table_data['H_OPEN'] * 100
    table_data['D_MAX'] = table_data['D_MAX'].round(3)
    table_data['D_MIN'] = table_data['D_MIN'].round(3)
    table_data['H_MAX'] = table_data['H_MAX'].round(3)
    table_data['H_MIN'] = table_data['H_MIN'].round(3)

    table_data['D_CHANGE'] = (table_data['price'] - table_data['D_OPEN'])/table_data['D_OPEN'] * 100
    table_data['D_C_MIN'] = (table_data['price'] - table_data['D_LOW'])/table_data['D_LOW'] * 100
    table_data['D_C_MAX'] = (table_data['price'] - table_data['D_HIGH'])/table_data['D_HIGH'] * 100
    table_data['H_CHANGE'] = (table_data['price'] - table_data['H_OPEN'])/table_data['H_OPEN'] * 100
    table_data['H_C_MIN'] = (table_data['price'] - table_data['H_LOW'])/table_data['H_LOW'] * 100
    table_data['H_C_MAX'] = (table_data['price'] - table_data['H_HIGH'])/table_data['H_HIGH'] * 100
    table_data['D_CHANGE'] = table_data['D_CHANGE'].round(3)                
    table_data['H_CHANGE'] = table_data['H_CHANGE'].round(3)
    table_data['D_C_MIN'] = table_data['D_C_MIN'].round(3)
    table_data['D_C_MAX'] = table_data['D_C_MAX'].round(3)
    table_data['H_C_MIN'] = table_data['H_C_MIN'].round(3)
    table_data['H_C_MAX'] = table_data['H_C_MAX'].round(3)

    day_df = table_data[['symbol','D_OPEN','D_HIGH','D_LOW','price','D_MAX','D_MIN','D_C_MAX','D_C_MIN','D_CHANGE']]
    day_df = day_df.sort_values('D_C_MIN',ascending=False)
    # print(tabulate(day_df.head(12), headers='keys', tablefmt='psql'))
    # print(tabulate(day_df.tail(12), headers='keys', tablefmt='psql'))
    #print(tabulate(day_df,headers='keys',tablefmt='psql'))
    up_df=day_df[day_df['D_C_MAX'] >= -0.2] 
    # up_df = up_df.drop(['D_HIGH','D_LOW','H_HIGH','H_LOW'],axis=1)
    up_df = up_df.sort_values(by=['D_C_MAX','D_CHANGE'],ascending=[False,False])
    down_df=day_df[day_df['D_C_MIN'] <= 0.2]
    # down_df = down_df.drop(['D_HIGH','D_LOW','H_HIGH','H_LOW'],axis=1)
    down_df = down_df.sort_values(by=['D_C_MIN','D_CHANGE'],ascending=[True,True])

    print(pyfiglet.figlet_format("UP", font="slant"))
    print(tabulate(up_df,headers='keys',tablefmt='psql'))
    print(pyfiglet.figlet_format("DOWN", font="slant"))
    print(tabulate(down_df,headers='keys',tablefmt='psql'))

    table_data = table_data.drop(['D_HIGH','D_LOW','H_HIGH','H_LOW'],axis=1)
    table_data = table_data[['symbol','D_OPEN','D_MAX','D_MIN','D_C_MAX','D_C_MIN','D_CHANGE','H_OPEN','H_MAX','H_MIN','H_C_MIN','H_C_MAX','H_CHANGE']]


    # print(table_data)

    # table_data = table_data.sort_values('H_C_MIN',ascending=False)
    # print(tabulate(table_data.head(12), headers='keys', tablefmt='psql'))
    # print(tabulate(table_data.tail(12), headers='keys', tablefmt='psql'))
    
    # table_data
    # table_data['max_change_d'] = table_data['max_change_d'].round(3)
    # table_data['min_change_d'] = table_data['min_change_d'].round(3)
    # table_data['max_change_h'] = table_data['max_change_h'].round(3)
    # table_data['min_change_h'] = table_data['min_change_h'].round(3)
    # table_data['price'] = table_data['price'].astype(float)
    # table_data['change_d'] = (table_data['price'] - table_data['Y_D_O_Price'])/table_data['Y_D_O_Price'] * 100
    # table_data['change_h'] = (table_data['price'] - table_data['Y_H_O_Price'])/table_data['Y_H_O_Price'] * 100

    #table_data = table_data.drop(['high_price_x','low_price_x','high_price_y','low_price_y'],axis=1)
    #print(tabulate(table_data, headers='keys', tablefmt='psql'))


    # table_data =table_data[['symbol','Y_D_Change','Y_D_C_Price','Y_H_Change','Y_H_C_Price','price']]
    # table_data['Y_D_C_Price'] = pd.to_numeric(table_data['Y_D_C_Price'], errors='coerce')
    # table_data['Y_H_C_Price'] = pd.to_numeric(table_data['Y_H_C_Price'], errors='coerce')
    # table_data['price'] = pd.to_numeric(table_data['price'], errors='coerce')
    # table_data ['day_change']= (table_data['price'] - table_data['Y_D_C_Price']) /table_data['Y_D_C_Price'] * 100
    # table_data ['hour_change']= (table_data['price'] - table_data['Y_H_C_Price']) /table_data['Y_H_C_Price'] * 100
    # table_data = table_data.sort_values('day_change',ascending=False)  
    # # print(tabulate(table_data, headers='keys', tablefmt='grid'))
    # print(tabulate(table_data.head(8), headers='keys', tablefmt='grid'))
    # print(tabulate(table_data.tail(8), headers='keys', tablefmt='grid'))
    # table_data = table_data.sort_values('hour_change',ascending=False)  
    # # print(tabulate(table_data, headers='keys', tablefmt='grid'))
    # print(tabulate(table_data.head(8), headers='keys', tablefmt='psql'))
    # print(tabulate(table_data.tail(8), headers='keys', tablefmt='psql'))
    

def get_data(new_data=False):
    global previous_day_df
    if not path.exists("hour.csv") or new_data:
        print("previous_data_not_found:")
        tickers = partha_account.futures_ticker()
        column_name_df = pd.DataFrame(tickers)
        column_name_df = column_name_df[column_name_df['symbol'].str.endswith(
            'USDT')]
        busd_list = column_name_df['symbol'].to_list()

        # ti_st = int(dt.datetime.now().timestamp())
        # time_stamp = int(ti_st - ti_st % 86400)
        # start_time = (time_stamp-86400) * 1000
        # end_time = (time_stamp*1000 - 1)
        coin_data = collections.deque([], maxlen=int(len(busd_list)/1))

        key_list = ["open_time", "open_price", "high_price", "low_price", "close_price",
                    "volume", "close_time", "asset_volume", "no_of_trades", "TBBAV", "TBQAV", "UNUSED"]
        data = 0
        for coin in busd_list:
            klines = partha_account.futures_historical_klines(
                coin, partha_account.KLINE_INTERVAL_2HOUR, "2 hour ago UTC")
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
        coin_data_df.to_csv("hour.csv")
        previous_day_df = coin_data_df[['symbol', 'open_price','high_price','low_price']]
        previous_day_df['high_price'] = previous_day_df['high_price'].astype(float)
        previous_day_df['open_price'] = previous_day_df['open_price'].astype(float)
        previous_day_df['low_price'] = previous_day_df['low_price'].astype(float)
        previous_day_df['max_change_d'] = (previous_day_df['high_price'] - previous_day_df['open_price']) / previous_day_df['open_price'] * 100
        previous_day_df['min_change'] = (previous_day_df['low_price'] - previous_day_df['open_price']) / previous_day_df['open_price'] * 100
        # previous_day_df['change'] = (previous_day_df['close_price'] - previous_day_df['open_price']) / previous_day_df['open_price'] * 100
        previous_day_df = previous_day_df[previous_day_df['symbol'].str.endswith(
            'USDT')]
        #previous_day_df = previous_day_df[~previous_day_df['symbol'].str.contains(1000')]
        # previous_day_df = previous_day_df.sort_values('change', ascending=False)
        return previous_day_df
    else:
        print("Previous_data_found: Reading from CSV file")
        coin_data_df = pd.read_csv("hour.csv")
        previous_day_df = coin_data_df[['symbol', 'open_price','high_price','low_price']]
        previous_day_df['high_price'] = previous_day_df['high_price'].astype(float)
        previous_day_df['open_price'] = previous_day_df['open_price'].astype(float)
        previous_day_df['low_price'] = previous_day_df['low_price'].astype(float)
        previous_day_df['max_change_d'] = (previous_day_df['high_price'] - previous_day_df['open_price']) / previous_day_df['open_price'] * 100
        previous_day_df['min_change_d'] = (previous_day_df['low_price'] - previous_day_df['open_price']) / previous_day_df['open_price'] * 100
        #previous_day_df['change'] = (previous_day_df['close_price'] - previous_day_df['open_price']) / previous_day_df['open_price'] * 100
        previous_day_df = previous_day_df[previous_day_df['symbol'].str.endswith(
            'USDT')]
        #previous_day_df = previous_day_df[~previous_day_df['symbol'].str.contains(1000')]
        #previous_day_df = previous_day_df.sort_values(change', ascending=False)
        return previous_day_df

def get_hour_data(new_data=False):
    global previous_hour_df
    if not path.exists("_data.csv") :
        print("previous_hour_data_not_found:")
        tickers = partha_account.futures_ticker()
        column_name_df = pd.DataFrame(tickers)
        column_name_df = column_name_df[column_name_df['symbol'].str.endswith(
            'USDT')]
        busd_list = column_name_df['symbol'].to_list()

        # ti_st = int(dt.datetime.now().timestamp())
        # time_stamp = int(ti_st - ti_st % 7200)
        # start_time = (time_stamp-7200) * 1000
        # end_time = (time_stamp*1000 - 1)
        coin_data = collections.deque([], maxlen=int(len(busd_list)/1))

        key_list = ["open_time", "open_price", "high_price", "low_price", "close_price",
                    "volume", "close_time", "asset_volume", "no_of_trades", "TBBAV", "TBQAV", "UNUSED"]
        data = 0
        for coin in busd_list:
            klines = partha_account.futures_historical_klines(
                coin, partha_account.KLINE_INTERVAL_2HOUR, "2 hour ago UTC")
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
        coin_data_df.to_csv("_data.csv")
        previous_hour_df = coin_data_df[['symbol','open_price','high_price','low_price']]
        previous_hour_df['high_price'] = previous_hour_df['high_price'].astype(float)
        previous_hour_df['open_price'] = previous_hour_df['open_price'].astype(float)
        previous_hour_df['low_price'] = previous_hour_df['low_price'].astype(float)
        previous_hour_df['max_change_h'] = (previous_hour_df['high_price'] - previous_hour_df['open_price']) / previous_hour_df['open_price'] * 100
        previous_hour_df['min_change_h'] = (previous_hour_df['low_price'] - previous_hour_df['open_price']) / previous_hour_df['open_price'] * 100
        # previous_hour_df['change'] = (previous_hour_df['close_price'] - previous_hour_df['open_price']) / previous_hour_df['open_price'] * 100
        previous_hour_df = previous_hour_df[previous_hour_df['symbol'].str.endswith(
            'USDT')]
        # previous_hour_df = previous_hour_df[~previous_hour_df['symbol'].str.contains(
        #     '1000')]
        # previous_hour_df = previous_hour_df.sort_values( 'change', ascending=False)
        return previous_hour_df
    elif (new_data == True):
        hour_tickers = partha_account.futures_symbol_ticker()
        hour_tickers_df = pd.DataFrame(hour_tickers)
        hour_tickers_df = hour_tickers_df[hour_tickers_df['symbol'].str.endswith('USDT')]
        hour_tickers_df = hour_tickers_df[['symbol','price']]
        return hour_tickers_df
    else:
        print("Previous_hour_data_found: Reading from CSV file")
        coin_data_df = pd.read_csv("_data.csv")
        previous_hour_df = coin_data_df[['symbol', 'open_price','high_price','low_price']]
        previous_hour_df['high_price'] = previous_hour_df['high_price'].astype(float)
        previous_hour_df['open_price'] = previous_hour_df['open_price'].astype(float)
        previous_hour_df['low_price'] = previous_hour_df['low_price'].astype(float)
        previous_hour_df['max_change_h'] = (previous_hour_df['high_price'] - previous_hour_df['open_price']) / previous_hour_df['open_price'] * 100
        previous_hour_df['min_change_h'] = (previous_hour_df['low_price'] - previous_hour_df['open_price']) / previous_hour_df['open_price'] * 100
        # previous_hour_df['change'] = (previous_hour_df['close_price'] - previous_hour_df['open_price']) / previous_hour_df['open_price'] * 100
        previous_hour_df = previous_hour_df[previous_hour_df['symbol'].str.endswith(
            'USDT')]
        # previous_hour_df = previous_hour_df[~previous_hour_df['symbol'].str.contains(
        #     '1000')]
        # previous_hour_df = previous_hour_df.sort_values('change', ascending=False)
        return previous_hour_df


print(pyfiglet.figlet_format("Binance Bot"))
previous_day_df = get_data()
previous_hour_df = get_hour_data()

sch.every().hour.at("30:00").do(get_data, new_data=True)
# sch.every().hour.at(":30").do(get_hour_data,new_data=True)
sch.every().minute.at(":05").do(get_tickers, partha_account=partha_account, yesterday_df=previous_day_df,yesterhour_df=previous_hour_df)
sch.every().minute.at(":35").do(get_tickers, partha_account=partha_account, yesterday_df=previous_day_df,yesterhour_df=previous_hour_df)

while True:
    sch.run_pending()
