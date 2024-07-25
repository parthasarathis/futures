from binance.client import Client
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
import streamlit as st
import requests
import numpy as np
import time
import datetime as dt
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Binance API endpoint for futures prices
endpoint = "https://fapi.binance.com/fapi/v1/klines"

# Set up the client
api_key = "FLPeS5t9QAntmcsEtYYv01JBZufM5SQQu751qh0s9rcHwVXZqioztxpMnyVMxvlP"
sec_key = "kP7twDqEL7alJGf4R4uDH6cNsivpscabZ4EEdD9SWJugC7DOJu7YHfcgeP8ngUJw"
partha_account = Client(api_key=api_key, api_secret=sec_key)

coin_price = collections.deque([], maxlen=20)

futures_type = FuturesType.USD_M

st.set_page_config(layout='wide')
pd.set_option('display.max_rows', 20)


possible_u, possible_d = st.columns(2)
possible_u_placeholder = possible_u.empty()
possible_d_placeholder = possible_d.empty()
possible_u_placeholder.text("Possible UP")
possible_d_placeholder.text("Possible DOWN")

possible_u_col, possible_d_col = st.columns(2)
possible_u_placeholder = possible_u_col.empty()
possible_d_placeholder = possible_d_col.empty()


all_u, all_d = st.columns(2)
all_u_placeholder = all_u.empty()
all_d_placeholder = all_d.empty()
all_u_placeholder.text("ALL UP")
all_d_placeholder.text("ALL DOWN")

up_col, down_col = st.columns(2)

up_placeholder = up_col.empty()
down_placeholder = down_col.empty()
# up1_placeholder = up1_col.empty()
# down1_placeholder = down1_col.empty()

pos_rev = st.empty()
pos_rev.text("Posible Reversal")

up2d, down2d = st.columns(2)
up2d_placeholder = up2d.empty()
down2d_placeholder = down2d.empty()
up2d_placeholder.text("UP TO DOWN")
down2d_placeholder.text("DOWN TO UP")

u2d, d2u = st.columns(2)
u2d_placeholder = u2d.empty()
d2u_placeholder = d2u.empty()

top_10_u, top_10_d = st.columns(2)
top_10_u_placeholder = top_10_u.empty()
top_10_d_placeholder = top_10_d.empty()
top_10_u_placeholder.text("TOP 10 UP")
top_10_d_placeholder.text("TOP 10 DOWN")

top_u, top_d = st.columns(2)
top_u_placeholder = top_u.empty()
top_d_placeholder = top_d.empty()

# write comments for below function


def get_tickers(partha_account, df_ins_tick):
    tickers = partha_account.futures_symbol_ticker()
    df_tickers = pd.DataFrame(tickers)
    df_tickers = df_tickers[df_tickers['symbol'].str.endswith('USDT')]
    # df_tickers = df_tickers[~df_tickers['symbol'].str.contains('1000')]
    df_tickers = df_tickers.sort_values('symbol')
    df_tickers = df_tickers.drop('time', axis=1)

    table_data = pd.merge(df_ins_tick, df_tickers, on='symbol')

    table_data = table_data.rename(columns={'openPrice': 'D_OPEN', 'highPrice': 'D_HIGH',
                                   'lowPrice': 'D_LOW', 'max_change_d': 'D_MAX', 'min_change_d': 'D_MIN'})
    # table_data = table_data.drop(['Y_D_O_Price','Y_H_O_Price'],axis=1)

    table_data['price'] = table_data['price'].astype(float)
    # print(table_data)

    table_data['D_HIGH'] = np.maximum(
        table_data['D_HIGH'], table_data['price'])
    table_data['D_LOW'] = np.minimum(table_data['D_LOW'], table_data['price'])
    table_data['D_MAX'] = (table_data['D_HIGH'] -
                           table_data['D_OPEN'])/table_data['D_OPEN'] * 100
    table_data['D_MIN'] = (table_data['D_LOW'] -
                           table_data['D_OPEN'])/table_data['D_OPEN'] * 100
    table_data['D_MAX'] = table_data['D_MAX'].round(3)
    table_data['D_MIN'] = table_data['D_MIN'].round(3)

    table_data['D_CHANGE'] = (table_data['price'] -
                              table_data['D_OPEN'])/table_data['D_OPEN'] * 100
    table_data['D_C_MIN'] = (table_data['price'] -
                             table_data['D_LOW'])/table_data['D_LOW'] * 100
    table_data['D_C_MAX'] = (table_data['price'] -
                             table_data['D_HIGH'])/table_data['D_HIGH'] * 100
    table_data['D_CHANGE'] = table_data['D_CHANGE'].round(3)
    table_data['D_C_MIN'] = table_data['D_C_MIN'].round(3)
    table_data['D_C_MAX'] = table_data['D_C_MAX'].round(3)

    actual_df = table_data[['symbol', 'D_CHANGE',
                            'D_MAX', 'D_MIN', 'D_C_MAX', 'D_C_MIN']]
    actual_df = actual_df.sort_values('D_CHANGE', ascending=False)

    day_df = table_data[['symbol', 'D_CHANGE',
                         'D_MAX', 'D_MIN', 'D_C_MAX', 'D_C_MIN']]
    day_df = day_df[day_df['D_MAX'] != 0]

    day_df = day_df.sort_values('D_C_MIN', ascending=False)
    # print(tabulate(day_df, headers='keys', tablefmt='psql'))
    up_df = day_df[day_df['D_MIN'] > - 0.5]
    up_df = up_df.sort_values('D_C_MIN', ascending=False)
    down_df = day_df[day_df['D_MAX'] < 0.5]
    down_df = down_df.sort_values('D_C_MAX', ascending=True)

    up1_df = day_df
    up1_df = up1_df[up1_df['D_C_MAX'] > -0.75]
    up1_df = up1_df.sort_values('D_C_MAX', ascending=False)
    up1_df.set_index('symbol', inplace=True)
    down1_df = day_df
    down1_df = down1_df[down1_df['D_C_MIN'] < 0.75]
    down1_df = down1_df.sort_values('D_C_MIN', ascending=True)
    down1_df.set_index('symbol', inplace=True)

    u_to_d = day_df[(day_df['D_C_MAX'] < -0.5) &
                    (day_df['D_C_MAX'] > -1.25) & (day_df['D_C_MIN'] > 3)]
    u_to_d = u_to_d.sort_values('D_C_MIN', ascending=False)
    d_to_u = day_df[(day_df['D_C_MIN'] > 0.5) &
                    (day_df['D_C_MIN'] < 1.25) & (day_df['D_C_MAX'] < - 3)]
    d_to_u = d_to_u.sort_values('D_C_MAX', ascending=True)

    top = actual_df[actual_df['D_CHANGE'] >= 0]
    top = top.sort_values('D_CHANGE', ascending=False)
    bottom = actual_df[actual_df['D_CHANGE'] < 0]
    bottom = bottom.sort_values('D_CHANGE', ascending=True)

    # Set symbol column as index in actual_df
    actual_df.set_index('symbol', inplace=True)

    # Apply conditions based on time
    if dt.datetime.now().time() < dt.time(8, 0):
        possible_up = actual_df[(actual_df['D_MIN'] < -0.5) & (actual_df['D_MIN'] > -6) & (
            actual_df['D_CHANGE'] > 0)].sort_values('D_CHANGE', ascending=False)
        possible_down = actual_df[(actual_df['D_MAX'] > 0.5) & (actual_df['D_MAX'] < 6) & (
            actual_df['D_CHANGE'] < 0)].sort_values('D_CHANGE', ascending=True)
    else:
        possible_up = actual_df[(actual_df['D_MIN'] < -0.5) & (actual_df['D_MIN'] > -6) & (
            actual_df['D_CHANGE'] > 2.0)].sort_values('D_CHANGE', ascending=False).head(10)
        possible_down = actual_df[(actual_df['D_MAX'] > 0.5) & (actual_df['D_MAX'] < 6) & (
            actual_df['D_CHANGE'] < -2.0)].sort_values('D_CHANGE', ascending=True).head(10)

    # Apply styling to possible_up and possible_down dataframes
    styled_possible_up = possible_up.style.applymap(lambda x: 'color: red' if x < 0 else 'color: green', subset=['D_CHANGE']).applymap(
        lambda x: 'color: violet' if x < -0.3 else 'color: blue', subset=['D_C_MAX']).applymap(lambda x: 'color: green' if x > -0.5 else 'color: red', subset=['D_MIN'])
    styled_possible_down = possible_down.style.applymap(lambda x: 'color: green' if x > 0 else 'color: red', subset=['D_CHANGE']).applymap(
        lambda x: 'color: violet' if x > 0.3 else 'color: blue', subset=['D_C_MIN']).applymap(lambda x: 'color: green' if x < 0.5 else 'color: red', subset=['D_MAX'])

    # Display the possible_up and possible_down dataframes
    possible_u_placeholder.text(
        "Possible UP" + " = " + str(len(possible_up)))
    possible_d_placeholder.text(
        "Possible DOWN" + " = " + str(len(possible_down)))
    possible_u_placeholder.dataframe(styled_possible_up, height=max(
        len(possible_up)*50, len(possible_up)*50))
    possible_d_placeholder.dataframe(styled_possible_down, height=max(
        len(possible_down)*50, len(possible_down)*50))

    # Sort and style the up and down dataframes
    up = up_df
    up = up.sort_values('D_C_MIN', ascending=False)
    down = down_df
    down = down.sort_values('D_C_MAX', ascending=True)
    up = up.round(3)
    down = down.round(3)

    # Apply styling to up and down dataframes
    styled_up = up.style.applymap(lambda x: 'color: red' if x < 0 else 'color: green', subset=['D_CHANGE']).applymap(
        lambda x: 'color: violet' if x < -0.3 else 'color: blue', subset=['D_C_MAX']).applymap(lambda x: 'color: green' if x > -0.5 else 'color: red', subset=['D_MIN'])
    styled_down = down.style.applymap(lambda x: 'color: green' if x > 0 else 'color: red', subset=['D_CHANGE']).applymap(
        lambda x: 'color: violet' if x > 0.3 else 'color: blue', subset=['D_C_MIN']).applymap(lambda x: 'color: green' if x < 0.5 else 'color: red', subset=['D_MAX'])

    # Display the up and down dataframes
    all_u_placeholder.text("##ALL UP" + " = " + str(len(up)))
    all_d_placeholder.text("##ALL DOWN" + " = " + str(len(down)))
    up_placeholder.dataframe(
        styled_up, height=max(len(up)*40, len(up)*40))
    down_placeholder.dataframe(
        styled_down, height=max(len(up)*40, len(down)*40))

    # Apply styling to u_to_d and d_to_u dataframes
    styled_up_2_d = u_to_d.style.applymap(lambda x: 'color: red' if x < 0 else 'color: green', subset=['D_CHANGE']).applymap(
        lambda x: 'color: violet' if x < -0.3 else 'color: blue', subset=['D_C_MAX']).applymap(lambda x: 'color: green' if x > -0.5 else 'color: red', subset=['D_MIN'])
    styled_down_to_u = d_to_u.style.applymap(lambda x: 'color: green' if x > 0 else 'color: red', subset=['D_CHANGE']).applymap(
        lambda x: 'color: violet' if x > 0.3 else 'color: blue', subset=['D_C_MIN']).applymap(lambda x: 'color: green' if x < 0.5 else 'color: red', subset=['D_MAX'])

    # Display the u_to_d and d_to_u dataframes
    up2d_placeholder.text("##UP TO DOWN" + " = " + str(len(u_to_d)))
    down2d_placeholder.text("##DOWN TO UP" + " = " + str(len(d_to_u)))
    u2d_placeholder.dataframe(
        styled_up_2_d, height=max(len(u_to_d)*50, len(d_to_u)*50))
    d2u_placeholder.dataframe(
        styled_down_to_u, height=max(len(u_to_d)*50, len(d_to_u)*50))

    # Display the top 15 up and down dataframes
    top_10_u_placeholder.text("##TOP 15 UP")
    top_10_d_placeholder.text("##TOP 15 DOWN")
    styled_top_u = top.head(20).style.applymap(lambda x: 'color: red' if x < 0 else 'color: green', subset=['D_CHANGE']).applymap(
        lambda x: 'color: violet' if x < -0.3 else 'color: blue', subset=['D_C_MAX']).applymap(lambda x: 'color: green' if x > -0.5 else 'color: red', subset=['D_MIN'])
    styled_top_d = bottom.head(20).style.applymap(lambda x: 'color: green' if x > 0 else 'color: red', subset=['D_CHANGE']).applymap(
        lambda x: 'color: violet' if x > 0.3 else 'color: blue', subset=['D_C_MIN']).applymap(lambda x: 'color: green' if x < 0.5 else 'color: red', subset=['D_MAX'])
    top_u_placeholder.dataframe(
        styled_top_u, height=20*50)
    top_d_placeholder.dataframe(
        styled_top_d, height=20*50)

    # Wait for 10 seconds
    time.sleep(10)

    # going_down = day_df[day_df['PCT'] < 20]
    # going_down = going_down.sort_values('D_C_MIN',ascending=True)
    # print(pyfiglet.figlet_format("going_down", font="slant"))
    # print(tabulate(going_down,headers='keys',tablefmt='psql'))

    # going_up = day_df[day_df['PCT'] > 85]
    # going_up = going_up.sort_values('D_C_MAX',ascending=False)
    # print(pyfiglet.figlet_format("going_up", font="slant"))
    # print(tabulate(going_up,headers='keys',tablefmt='psql'))


def initialise(partha_account):
    print(pyfiglet.figlet_format("Initialised" +
          dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    tickers = partha_account.futures_symbol_ticker()
    ins_tick = pd.DataFrame(tickers)
    ins_tick = ins_tick[ins_tick['symbol'].str.endswith('USDT')]
# ins_tick = ins_tick[~ins_tick['symbol'].str.contains('1000')]
    ins_tick["highPrice"] = ins_tick["price"].astype(float)
    ins_tick["lowPrice"] = ins_tick["price"].astype(float)
    ins_tick["openPrice"] = ins_tick["price"].astype(float)

    ins_tick['max_change_d'] = (
        ins_tick['highPrice'] - ins_tick['openPrice']) / ins_tick['openPrice'] * 100
    ins_tick['min_change'] = (
        ins_tick['lowPrice'] - ins_tick['openPrice']) / ins_tick['openPrice'] * 100
    ins_tick = ins_tick.drop('price', axis=1)
    ins_tick = ins_tick.drop('time', axis=1)
    return ins_tick


print(pyfiglet.figlet_format("Binance Bot"))
ins_tick = initialise(partha_account)

# print(tabulate(ins_tick, headers='keys', tablefmt='psql'))


while True:
    current_time = dt.datetime.now().time()
    if current_time.hour in [1, 5, 9, 13, 17, 21] and current_time.minute == 30:
        initialise(partha_account)
    get_tickers(partha_account, ins_tick)
