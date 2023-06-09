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
def get_tickers(partha_account,df_ins_tick):
    tickers = partha_account.futures_symbol_ticker()
    df_tickers = pd.DataFrame(tickers)
    df_tickers = df_tickers[df_tickers['symbol'].str.endswith('USDT')]
    #df_tickers = df_tickers[~df_tickers['symbol'].str.contains('1000')]
    df_tickers = df_tickers.sort_values('symbol')
    df_tickers = df_tickers.drop('time', axis=1)



    table_data = pd.merge(df_tickers, df_ins_tick, on='symbol', how='left')
    table_data = table_data.rename(columns={'openPrice': 'D_OPEN', 'highPrice': 'D_HIGH', 'lowPrice': 'D_LOW','price':'C_PRICE'})
    print(tabulate(table_data, headers='keys', tablefmt='psql'))

    table_data['C_PRICE'] = table_data['C_PRICE'].astype(float)
    table_data['D_HIGH']=np.maximum(table_data['D_HIGH'],table_data['C_PRICE'])
    table_data['D_LOW']=np.minimum(table_data['D_LOW'],table_data['C_PRICE'])
    table_data['D_MAX'] = (table_data['D_HIGH'] - table_data['D_OPEN'])/table_data['D_OPEN'] * 100
    table_data['D_MIN'] = (table_data['D_LOW'] - table_data['D_OPEN'])/table_data['D_OPEN'] * 100 
    table_data['PCT'] = ((table_data['C_PRICE'] - table_data['D_LOW']) / (table_data['D_HIGH'] - table_data['D_LOW'])) * 100
    table_data['PCT'] = table_data['PCT'].round(2)
    table_data['PCT'] = table_data['PCT'].astype(float)
    table_data['D_MAX'] = table_data['D_MAX'].round(3)
    table_data['D_MIN'] = table_data['D_MIN'].round(3)


    table_data['D_CHANGE'] = (table_data['C_PRICE'] - table_data['D_OPEN'])/table_data['D_OPEN'] * 100
    table_data['D_C_MIN'] = (table_data['C_PRICE'] - table_data['D_LOW'])/table_data['D_LOW'] * 100
    table_data['D_C_MAX'] = (table_data['C_PRICE'] - table_data['D_HIGH'])/table_data['D_HIGH'] * 100
    table_data['D_CHANGE'] = table_data['D_CHANGE'].round(3)                
    table_data['D_C_MIN'] = table_data['D_C_MIN'].round(3)
    table_data['D_C_MAX'] = table_data['D_C_MAX'].round(3)
   
    day_df = table_data[['symbol','D_OPEN','D_HIGH','D_LOW','C_PRICE','D_MAX','D_MIN','D_C_MAX','D_C_MIN','PCT','D_CHANGE']]
    day_df = day_df.sort_values('D_C_MIN',ascending=False)
    day_df['PCT'] = day_df['PCT'].round(2)

    print("\033c", end="")

    up_df = day_df.sort_values('D_C_MIN',ascending=False)
    down_df = day_df.sort_values('D_C_MAX',ascending=True)

    print(pyfiglet.figlet_format("UP"))
    print(tabulate(up_df.head(10), headers='keys', tablefmt='psql'))
    print(pyfiglet.figlet_format("DOWN"))
    print(tabulate(down_df.head(10), headers='keys', tablefmt='psql'))




print(pyfiglet.figlet_format("Binance Bot"))

tickers = partha_account.futures_symbol_ticker()
ins_tick = pd.DataFrame(tickers)
ins_tick = ins_tick[ins_tick['symbol'].str.endswith('USDT')]
#ins_tick = ins_tick[~ins_tick['symbol'].str.contains('1000')]
ins_tick["highPrice"] = ins_tick["price"].astype(float)
ins_tick["lowPrice"] = ins_tick["price"].astype(float)
ins_tick["openPrice"] = ins_tick["price"].astype(float)
ins_tick = ins_tick.drop('price', axis=1)
ins_tick = ins_tick.drop('time', axis=1)


#print(tabulate(ins_tick, headers='keys', tablefmt='psql'))


sch.every().minute.at(":05").do(get_tickers, partha_account=partha_account,df_ins_tick=ins_tick)
sch.every().minute.at(":10").do(get_tickers, partha_account=partha_account,df_ins_tick=ins_tick)
sch.every().minute.at(":15").do(get_tickers, partha_account=partha_account,df_ins_tick=ins_tick)
sch.every().minute.at(":20").do(get_tickers, partha_account=partha_account,df_ins_tick=ins_tick)
sch.every().minute.at(":25").do(get_tickers, partha_account=partha_account,df_ins_tick=ins_tick)
sch.every().minute.at(":30").do(get_tickers, partha_account=partha_account,df_ins_tick=ins_tick)
sch.every().minute.at(":35").do(get_tickers, partha_account=partha_account,df_ins_tick=ins_tick)
sch.every().minute.at(":40").do(get_tickers, partha_account=partha_account,df_ins_tick=ins_tick)
sch.every().minute.at(":45").do(get_tickers, partha_account=partha_account,df_ins_tick=ins_tick)
sch.every().minute.at(":50").do(get_tickers, partha_account=partha_account,df_ins_tick=ins_tick)
sch.every().minute.at(":55").do(get_tickers, partha_account=partha_account,df_ins_tick=ins_tick)
sch.every().minute.at(":00").do(get_tickers, partha_account=partha_account,df_ins_tick=ins_tick)

while True:
    sch.run_pending()
