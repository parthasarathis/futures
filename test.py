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
def get_tickers(partha_account,yesterday_df):
    tickers = partha_account.futures_symbol_ticker()
    df_tickers = pd.DataFrame(tickers)
    df_tickers = df_tickers[df_tickers['symbol'].str.endswith('USDT')]
    df_tickers = df_tickers[~df_tickers['symbol'].str.contains('1000')]
    df_tickers = df_tickers.sort_values('symbol')
    df_tickers = df_tickers.drop('time', axis=1)

  
    table_data = pd.merge(yesterday_df,df_tickers,on='symbol')

    table_data = table_data.rename(columns={'open_price': 'D_OPEN', 'high_price': 'D_HIGH', 'low_price': 'D_LOW','max_change_d': 'D_MAX','min_change_d': 'D_MIN'})
    table_data['price'] = pd.to_numeric(table_data['price'], errors='coerce')
    table_data['D_LOW'] = pd.to_numeric(table_data['D_LOW'], errors='coerce')
    table_data['D_HIGH'] = pd.to_numeric(table_data['D_HIGH'], errors='coerce')
    
    # table_data = table_data.drop(['Y_D_O_Price','Y_H_O_Price'],axis=1)
    
    table_data['price'] = table_data['price'].astype(float)
    # print(table_data)

    table_data['D_HIGH']=np.maximum(table_data['D_HIGH'],table_data['price'])
    table_data['D_LOW']=np.minimum(table_data['D_LOW'],table_data['price'])
    table_data['D_MAX'] = (table_data['D_HIGH'] - table_data['D_OPEN'])/table_data['D_OPEN'] * 100
    table_data['D_MIN'] = (table_data['D_LOW'] - table_data['D_OPEN'])/table_data['D_OPEN'] * 100 
    table_data['PCT'] = ((table_data['price'] - table_data['D_LOW']) / (table_data['D_HIGH'] - table_data['D_LOW'])) * 100
    table_data['PCT'] = table_data['PCT'].round(2)
    table_data['PCT'] = table_data['PCT'].astype(float)
    table_data['D_MAX'] = table_data['D_MAX'].round(3)
    table_data['D_MIN'] = table_data['D_MIN'].round(3)


    table_data['D_CHANGE'] = (table_data['price'] - table_data['D_OPEN'])/table_data['D_OPEN'] * 100
    table_data['D_C_MIN'] = (table_data['price'] - table_data['D_LOW'])/table_data['D_LOW'] * 100
    table_data['D_C_MAX'] = (table_data['price'] - table_data['D_HIGH'])/table_data['D_HIGH'] * 100
    table_data['D_CHANGE'] = table_data['D_CHANGE'].round(3)                
    table_data['D_C_MIN'] = table_data['D_C_MIN'].round(3)
    table_data['D_C_MAX'] = table_data['D_C_MAX'].round(3)
   
    day_df = table_data[['symbol','D_OPEN','D_HIGH','D_LOW','price','D_MAX','D_MIN','D_C_MAX','D_C_MIN','PCT','D_CHANGE']]
    day_df = day_df.sort_values('D_C_MIN',ascending=False)
    day_df['PCT'] = day_df['PCT'].round(2)

    print("\033c", end="")
    # print(tabulate(day_df,headers='keys',tablefmt='psql'))
   

    always_up = day_df[(day_df['D_C_MIN'] < 50) & (day_df['D_MIN']>-0.5)]
    print(pyfiglet.figlet_format("Always Up"))
    print(tabulate(always_up,headers='keys',tablefmt='psql'))

    always_down = day_df[(day_df['D_C_MAX'] > -50) & (day_df['D_MAX']<0.5)]
    print(pyfiglet.figlet_format("Always Down"))
    print(tabulate(always_down,headers='keys',tablefmt='psql'))

    up=day_df[(day_df['PCT'] > 80)]
    up = up.sort_values(by=['D_C_MIN','D_CHANGE'],ascending=[False,False])
    print(pyfiglet.figlet_format("Going Up"))
    print(tabulate(up,headers='keys',tablefmt='psql'))

    down=day_df[(day_df['PCT'] < 20)]
    down = down.sort_values(by=['D_C_MAX','D_CHANGE'],ascending=[True,True])
    print(pyfiglet.figlet_format("Going Down"))
    print(tabulate(down,headers='keys',tablefmt='psql'))

    #print(tabulate(day_df,headers='keys',tablefmt='psql'))
    up_df=day_df[(day_df['D_C_MIN'] < 50) & (day_df['D_C_MIN'] > 2) & (day_df['D_MIN']>-0.5)] 
    up_df = up_df.sort_values(by=['D_C_MIN','D_CHANGE'],ascending=[False,False])
    up_df['Status'] = up_df['PCT'].apply(lambda x: 'going down' if   x < 78.6 else 'up')
    down_df=day_df[(day_df['D_C_MAX'] > -50) & (day_df['D_C_MAX'] < -2) & (day_df['D_MAX']<0.5)]
    down_df = down_df.sort_values(by=['D_C_MAX','D_CHANGE'],ascending=[True,True])
    down_df['Status'] = down_df['PCT'].apply(lambda x: 'going up' if  x > 23.6 else 'down')



    # filtered_df = df[(df['column1'] > 10) & (df['column2'] == 'value')]

    down_2_up = day_df[(day_df['D_C_MIN'] > 2.5) & (day_df['D_C_MIN'] < 1)]
    down_2_up = down_2_up.sort_values(by=['D_C_MIN','D_CHANGE'],ascending=[False,False])
    up_2_down = day_df[(day_df['D_C_MAX'] < -2.5) & (day_df['D_C_MAX'] > -1)]
    up_2_down = up_2_down.sort_values(by=['D_C_MAX','D_CHANGE'],ascending=[True,True])

    # print(pyfiglet.figlet_format("down_2_up" , font = "slant"))
    # print(tabulate(down_2_up,headers='keys',tablefmt='psql'))
    # print(pyfiglet.figlet_format("up_2_down" , font = "slant"))
    # print(tabulate(up_2_down,headers='keys',tablefmt='psql'))


    # print(pyfiglet.figlet_format("GOING UP" , font = "slant"))
    # print(tabulate(up_df,headers='keys',tablefmt='psql'))
    # print(pyfiglet.figlet_format("GOING DOWN" , font = "slant"))
    # print(tabulate(down_df,headers='keys',tablefmt='psql'))

    table_data.to_csv('total_data.csv',index=True)
    up_df.to_csv('up_df.csv',index=True)
    down_df.to_csv('down_df.csv',index=True)
    

def get_data(new_data=False):
    global previous_day_df
    if not path.exists("previous_day_data.csv") or new_data:
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
                coin, partha_account.KLINE_INTERVAL_1DAY, "1 day ago UTC")
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
        previous_day_df = coin_data_df[['symbol', 'open_price','high_price','low_price']]
        previous_day_df['high_price'] = previous_day_df['high_price'].astype(float)
        previous_day_df['open_price'] = previous_day_df['open_price'].astype(float)
        previous_day_df['low_price'] = previous_day_df['low_price'].astype(float)
        previous_day_df['max_change_d'] = (previous_day_df['high_price'] - previous_day_df['open_price']) / previous_day_df['open_price'] * 100
        previous_day_df['min_change_d'] = (previous_day_df['low_price'] - previous_day_df['open_price']) / previous_day_df['open_price'] * 100
        # previous_day_df['change'] = (previous_day_df['close_price'] - previous_day_df['open_price']) / previous_day_df['open_price'] * 100
        previous_day_df = previous_day_df[previous_day_df['symbol'].str.endswith(
            'USDT')]
        #previous_day_df = previous_day_df[~previous_day_df['symbol'].str.contains(1000')]
        # previous_day_df = previous_day_df.sort_values('change', ascending=False)
        return previous_day_df
    else:
        print("Previous_data_found: Reading from CSV file")
        coin_data_df = pd.read_csv("previous_day_data.csv")
        previous_day_df = coin_data_df[['symbol', 'open_price','high_price','low_price']]

        previous_day_df['high_price'] = pd.to_numeric(previous_day_df['high_price'], errors='coerce')
        previous_day_df['low_price'] = pd.to_numeric(previous_day_df['low_price'], errors='coerce')
        previous_day_df['open_price'] = pd.to_numeric(previous_day_df['open_price'], errors='coerce')

        previous_day_df['max_change_d'] = (previous_day_df['high_price'] - previous_day_df['open_price']) / previous_day_df['open_price'] * 100
        previous_day_df['min_change_d'] = (previous_day_df['low_price'] - previous_day_df['open_price']) / previous_day_df['open_price'] * 100
        #previous_day_df['change'] = (previous_day_df['close_price'] - previous_day_df['open_price']) / previous_day_df['open_price'] * 100
        previous_day_df = previous_day_df[previous_day_df['symbol'].str.endswith(
            'USDT')]
        #previous_day_df = previous_day_df[~previous_day_df['symbol'].str.contains(1000')]
        #previous_day_df = previous_day_df.sort_values(change', ascending=False)
        return previous_day_df





print(pyfiglet.figlet_format("Binance Bot"))
previous_day_df = get_data()

sch.every().day.at("05:30").do(get_data, new_data=True)
sch.every().day.at("09:30").do(get_data, new_data=True)
sch.every().day.at("13:30").do(get_data, new_data=True)
sch.every().day.at("17:30").do(get_data, new_data=True)
sch.every().day.at("21:30").do(get_data, new_data=True)
sch.every().day.at("01:30").do(get_data, new_data=True)
sch.every().minute.at(":05").do(get_tickers, partha_account=partha_account, yesterday_df=previous_day_df)
sch.every().minute.at(":25").do(get_tickers, partha_account=partha_account, yesterday_df=previous_day_df)
sch.every().minute.at(":45").do(get_tickers, partha_account=partha_account, yesterday_df=previous_day_df)

while True:
    sch.run_pending()
