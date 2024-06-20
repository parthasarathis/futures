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
import matplotlib.pyplot as plt
import plotly.graph_objects as go

usdt_list = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "DOTUSDT",
    "SOLUSDT", "XRPUSDT", "LINKUSDT", "LTCUSDT", "BCHUSDT",
    "AVAXUSDT", "ALGOUSDT", "ATOMUSDT", "MATICUSDT", "XTZUSDT",
    "FILUSDT", "VETUSDT", "TRXUSDT", "THETAUSDT", "ETCUSDT",
    "NEOUSDT", "IOTAUSDT", "DASHUSDT", "CHZUSDT", "FTMUSDT",
    "KSMUSDT", "ZECUSDT", "COMPUSDT", "SUSHIUSDT", "EGLDUSDT",
    "WAVESUSDT", "ONEUSDT", "HBARUSDT", "FLOWUSDT", "RVNUSDT",
    "ENJUSDT", "ZRXUSDT", "SUIUSDT", "MANAUSDT", "STMXUSDT",
]


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


six_positive_placeholder = st.empty()
six_negative_placeholder = st.empty()
five_positive_placeholder = st.empty()
five_negative_placeholder = st.empty()
four_positive_placeholder = st.empty()
four_negative_placeholder = st.empty()
three_positive_placeholder = st.empty()
three_negative_placeholder = st.empty()
two_positive_placeholder = st.empty()
two_negative_placeholder = st.empty()


one_positive_placeholder = st.empty()
one_negative_placeholder = st.empty()
styled_df_combined_placeholder = st.empty()


up_title = st.empty()
down_title = st.empty()
up1_title = st.empty()
down1_title = st.empty()


# write comments for below function


def get_tickers(partha_account, yesterday_df):
    tickers = partha_account.futures_symbol_ticker()
    df_tickers = pd.DataFrame(tickers)
    df_tickers = df_tickers[df_tickers['symbol'].str.endswith('USDT')]
    df_tickers = df_tickers[~df_tickers['symbol'].str.contains('1000')]
    df_tickers = df_tickers.sort_values('symbol')
    df_tickers = df_tickers.drop('time', axis=1)

    table_data = pd.merge(yesterday_df, df_tickers, on='symbol')

    table_data = table_data.rename(columns={'open_price': 'D_OPEN', 'high_price': 'D_HIGH',
                                   'low_price': 'D_LOW', 'max_change_d': 'D_MAX', 'min_change_d': 'D_MIN'})
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

    actual_df = table_data[['symbol', 'D_CHANGE', 'D_OPEN', 'price']]
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

    up_to_down = day_df[(day_df['D_C_MAX'] < -0.5) &
                        (day_df['D_C_MAX'] > -1.25) & (day_df['D_C_MIN'] > 3)]
    up_to_down = up_to_down.sort_values('D_C_MIN', ascending=False)
    down_to_up = day_df[(day_df['D_C_MIN'] > 0.5) &
                        (day_df['D_C_MIN'] < 1.25) & (day_df['D_C_MAX'] < - 3)]
    down_to_up = down_to_up.sort_values('D_C_MAX', ascending=True)

    return up_df, down_df, up1_df, down1_df, table_data, actual_df, up_to_down, down_to_up
    # print(pyfiglet.figlet_format("UP", font="slant"))
    # print(tabulate(up_df.head(20), headers='keys', tablefmt='psql'))
    # print(pyfiglet.figlet_format("DOWN", font="slant"))
    # print(tabulate(down_df.head(20), headers='keys', tablefmt='psql'))

    # print(pyfiglet.figlet_format("Moving UP", font="slant"))
    # print(tabulate(up1_df.head(25), headers='keys', tablefmt='psql'))
    # print(pyfiglet.figlet_format("Moving DOWN", font="slant"))
    # print(tabulate(down1_df.head(25), headers='keys', tablefmt='psql'))


def get_data(new_data=False):
    global previous_day_df
    if not path.exists("previous_day_data.csv") or new_data:
        print("previous_data_not_found:")
        tickers = partha_account.futures_ticker()
        column_name_df = pd.DataFrame(tickers)
        column_name_df = column_name_df[column_name_df['symbol'].str.endswith(
            'USDT')]
        busd_list = column_name_df['symbol'].tolist()
        # busd_list = usdt_list

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
            print(coin)
            coin_data.append(res)
        coin_data_df = pd.DataFrame(coin_data)
        coin_data_df.to_csv("previous_day_data.csv")
        previous_day_df = coin_data_df[[
            'symbol', 'open_price', 'high_price', 'low_price']]
        previous_day_df['high_price'] = previous_day_df['high_price'].astype(
            float)
        previous_day_df['open_price'] = previous_day_df['open_price'].astype(
            float)
        previous_day_df['low_price'] = previous_day_df['low_price'].astype(
            float)
        previous_day_df['max_change_d'] = (
            previous_day_df['high_price'] - previous_day_df['open_price']) / previous_day_df['open_price'] * 100
        previous_day_df['min_change'] = (
            previous_day_df['low_price'] - previous_day_df['open_price']) / previous_day_df['open_price'] * 100
        # previous_day_df['change'] = (previous_day_df['close_price'] - previous_day_df['open_price']) / previous_day_df['open_price'] * 100
        previous_day_df = previous_day_df[previous_day_df['symbol'].str.endswith(
            'USDT')]
        # previous_day_df = previous_day_df[~previous_day_df['symbol'].str.contains(1000')]
        # previous_day_df = previous_day_df.sort_values('change', ascending=False)
        return previous_day_df
    else:
        print("Previous_data_found: Reading from CSV file")
        coin_data_df = pd.read_csv("previous_day_data.csv")
        previous_day_df = coin_data_df[[
            'symbol', 'open_price', 'high_price', 'low_price']]
        previous_day_df['high_price'] = previous_day_df['high_price'].astype(
            float)
        previous_day_df['open_price'] = previous_day_df['open_price'].astype(
            float)
        previous_day_df['low_price'] = previous_day_df['low_price'].astype(
            float)
        previous_day_df['max_change_d'] = (
            previous_day_df['high_price'] - previous_day_df['open_price']) / previous_day_df['open_price'] * 100
        previous_day_df['min_change_d'] = (
            previous_day_df['low_price'] - previous_day_df['open_price']) / previous_day_df['open_price'] * 100
        # previous_day_df['change'] = (previous_day_df['close_price'] - previous_day_df['open_price']) / previous_day_df['open_price'] * 100
        previous_day_df = previous_day_df[previous_day_df['symbol'].str.endswith(
            'USDT')]
        # previous_day_df = previous_day_df[~previous_day_df['symbol'].str.contains(1000')]
        # previous_day_df = previous_day_df.sort_values(change', ascending=False)
        return previous_day_df


def Today_data():
    st.title("TODAY DATA")

    while True:
        up_df, down_df, up1_df, down1_df, table_data, actual_df, u_to_d, d_to_u = get_tickers(
            partha_account, previous_day_df)

    # Sort the dataframes
        # up = actual_df[actual_df['D_CHANGE'] > 0]
        # up = up.sort_values('D_CHANGE', ascending=False)
        # down = actual_df[actual_df['D_CHANGE'] < 0]
        # down = down.sort_values('D_CHANGE', ascending=True)
        # up1_df = up1_df.sort_values('D_C_MAX', ascending=False)
        # down1_df = down1_df.sort_values('D_C_MIN', ascending=True)

        up = up_df
        up = up.sort_values('D_C_MIN', ascending=False)
        down = down_df
        down = down.sort_values('D_C_MAX', ascending=True)

        up = up.round(3)
        down = down.round(3)

        # Apply style to multiple columns with different conditions
        styled_up = up.style.applymap(
            lambda x: 'color: red' if x < 0 else 'color: green', subset=['D_CHANGE'])

        styled_up = styled_up.applymap(
            lambda x:  'color: violet' if x < -0.3 else 'color: blue', subset=['D_C_MAX'])

        styled_up = styled_up.applymap(
            lambda x: 'color: green' if x > -0.5 else 'color: red', subset=['D_MIN'])

        styled_down = down.style.applymap(
            lambda x: 'color: green' if x > 0 else 'color: red', subset=['D_CHANGE'])

        styled_down = styled_down.applymap(
            lambda x: 'color: violet' if x > 0.3 else 'color: blue', subset=['D_C_MIN'])

        styled_down = styled_down.applymap(
            lambda x: 'color: green' if x < 0.5 else 'color: red', subset=['D_MAX'])

        all_u_placeholder.text("ALL UP" + " = " + str(len(up)))
        all_d_placeholder.text("ALL DOWN" + " = " + str(len(down)))

        # Display the dataframes in their respective placeholders
        up_placeholder.dataframe(
            styled_up, height=max(len(up)*40, len(down)*40))
        down_placeholder.dataframe(
            styled_down, height=max(len(up)*40, len(down)*40))

        # up_placeholder.dataframe(up.head(20))

        # down_placeholder.dataframe(down.head(20))

        # up1_placeholder.dataframe(up1_df.head(20))

        # down1_placeholder.dataframe(down1_df.head(20))
        styled_up_2_d = u_to_d.style.applymap(
            lambda x: 'color: red' if x < 0 else 'color: green', subset=['D_CHANGE'])

        styled_up_2_d = styled_up_2_d.applymap(
            lambda x:  'color: violet' if x < -0.3 else 'color: blue', subset=['D_C_MAX'])

        styled_up_2_d = styled_up_2_d.applymap(
            lambda x: 'color: green' if x > -0.5 else 'color: red', subset=['D_MIN'])

        styled_down_to_u = d_to_u.style.applymap(
            lambda x: 'color: green' if x > 0 else 'color: red', subset=['D_CHANGE'])

        styled_down_to_u = styled_down_to_u.applymap(
            lambda x: 'color: violet' if x > 0.3 else 'color: blue', subset=['D_C_MIN'])

        styled_down_to_u = styled_down_to_u.applymap(
            lambda x: 'color: green' if x < 0.5 else 'color: red', subset=['D_MAX'])

        up2d_placeholder.text("UP TO DOWN" + " = " + str(len(u_to_d)))
        down2d_placeholder.text("DOWN TO UP" + " = " + str(len(d_to_u)))

        u2d_placeholder.dataframe(
            styled_up_2_d, height=max(len(u_to_d)*40, len(d_to_u)*40))
        d2u_placeholder.dataframe(
            styled_down_to_u, height=max(len(u_to_d)*40, len(d_to_u)*40))

        # Wait for 5 seconds
        time.sleep(5)


def ten_day_data():
    st.title("Previous 10 day DATA")
    df_data = pd.DataFrame()
    # Assuming df_data is the DataFrame you want to modify
    df_data = df_combined.sort_values(
        by=df_combined.index[-1], axis=1, ascending=False)
    df_data = df_data.transpose()
    df_data = df_data.drop("Unnamed: 0", errors='ignore')
    styled_df_combined = df_data.style.applymap(
        lambda x: 'color: red' if x < 0 else 'color: green')
# Display the styled DataFrame
    # styled_df_combined_placeholder.dataframe(styled_df_combined)

    one_positive = df_data[(
        df_data.iloc[:, -1:].gt(0).all(axis=1)) & (df_data.iloc[:, -2].lt(0))]
    one_positive = one_positive.sort_values(
        by=one_positive.columns[-1], ascending=False)
    one_positive1 = one_positive.style.applymap(
        lambda x: 'color: green' if x > 0 else 'color: red')

    one_negative = df_data[(
        df_data.iloc[:, -1:].lt(0).all(axis=1)) & (df_data.iloc[:, -2].gt(0))]
    one_negative = one_negative.sort_values(
        by=one_negative.columns[-1], ascending=True)
    one_negative1 = one_negative.style.applymap(
        lambda x: 'color: green' if x > 0 else 'color: red')

    two_positive = df_data[(
        df_data.iloc[:, -2:].gt(0).all(axis=1)) & (df_data.iloc[:, -3].lt(0))]
    two_positive = two_positive.sort_values(
        by=two_positive.columns[-1], ascending=False)
    two_positive1 = two_positive.style.applymap(
        lambda x: 'color: green' if x > 0 else 'color: red')

    two_negative = df_data[(
        df_data.iloc[:, -2:].lt(0).all(axis=1)) & (df_data.iloc[:, -3].gt(0))]
    two_negative = two_negative.sort_values(
        by=two_negative.columns[-1], ascending=True)
    two_negative1 = two_negative.style.applymap(
        lambda x: 'color: green' if x > 0 else 'color: red')

    three_positive = df_data[(
        df_data.iloc[:, -3:].gt(0).all(axis=1)) & (df_data.iloc[:, -4].lt(0))]
    three_positive = three_positive.sort_values(
        by=three_positive.columns[-1], ascending=False)
    three_positive1 = three_positive.style.applymap(
        lambda x: 'color: green' if x > 0 else 'color: red')

    three_negative = df_data[(
        df_data.iloc[:, -3:].lt(0).all(axis=1)) & (df_data.iloc[:, -4].gt(0))]
    three_negative = three_negative.sort_values(
        by=three_negative.columns[-1], ascending=True)
    three_negative1 = three_negative.style.applymap(
        lambda x: 'color: green' if x > 0 else 'color: red')

    four_positive = df_data[df_data.iloc[:, -4:].gt(0).all(axis=1)]
    four_positive = four_positive.sort_values(
        by=four_positive.columns[-1], ascending=False)
    four_positive1 = four_positive.style.applymap(
        lambda x: 'color: green' if x > 0 else 'color: red')

    four_negative = df_data[df_data.iloc[:, -4:].lt(0).all(axis=1)]
    four_negative = four_negative.sort_values(
        by=four_negative.columns[-1], ascending=True)
    four_negative1 = four_negative.style.applymap(
        lambda x: 'color: green' if x > 0 else 'color: red')

    five_positive = df_data[df_data.iloc[:, -5:].gt(0).all(axis=1)]
    five_positive = five_positive.sort_values(
        by=five_positive.columns[-1], ascending=False)
    five_positive1 = five_positive.style.applymap(
        lambda x: 'color: green' if x > 0 else 'color: red')

    five_negative = df_data[df_data.iloc[:, -5:].lt(0).all(axis=1)]
    five_negative = five_negative.sort_values(
        by=five_negative.columns[-1], ascending=True)
    five_negative1 = five_negative.style.applymap(
        lambda x: 'color: green' if x > 0 else 'color: red')

    six_positive = df_data[df_data.iloc[:, -6:].gt(0).all(axis=1)]
    six_positive = six_positive.sort_values(
        by=six_positive.columns[-1], ascending=False)
    six_positive1 = six_positive.style.applymap(
        lambda x: 'color: green' if x > 0 else 'color: red')

    six_negative = df_data[df_data.iloc[:, -6:].lt(0).all(axis=1)]
    six_negative = six_negative.sort_values(
        by=six_negative.columns[-1], ascending=True)
    six_negative1 = six_negative.style.applymap(
        lambda x: 'color: green' if x > 0 else 'color: red')

    st.write("## six +VE")
    st.dataframe(six_positive1)
    for index in six_positive.iterrows():
        st.button(f'Button {index}')
    st.write("## six -VE")
    st.dataframe(six_negative1)
    st.write("## five +VE")
    st.dataframe(five_positive1)
    st.write("## five -VE")
    st.dataframe(five_negative1)
    st.write("## four +VE")
    st.dataframe(four_positive1)
    st.write("## four -VE")
    st.dataframe(four_negative1)
    st.write("## three +VE")
    st.dataframe(three_positive1)
    st.write("## three -VE")
    st.dataframe(three_negative1)
    st.write("## two +VE")
    st.dataframe(two_positive1)
    st.write("## two -VE")
    st.dataframe(two_negative1)
    st.write("## one +VE")
    st.dataframe(one_positive1)
    st.write("## one -VE")
    st.dataframe(one_negative1)


def chart_data():
    st.title("Page 3")
    coin_name = st.text_input("Enter coin name")
    button_clicked = st.button("Get Data")
    interval = "1w"
    interval_1 = "1d"
    interval_2 = "4h"
    interval_3 = "1h"
    interval_4 = "15m"
    limit1 = 10
    limit2 = 14
    limit3 = 12
    limit4 = 16
    limit5 = 16

    if button_clicked:
        # Call a function to get data for the entered coin name
        # Pass the coin_name variable as an argument to the function
        # Example: get_coin_data(coin_name)
        # Replace get_coin_data with the actual function name you want to call
        params = {"symbol": coin_name, "interval": interval, "limit": limit1}
        response = requests.get(endpoint, params=params)
        data = response.json()
        params = {"symbol": coin_name, "interval": interval_1, "limit": limit2}
        response = requests.get(endpoint, params=params)
        data_1d = response.json()
        params = {"symbol": coin_name, "interval": interval_2, "limit": limit3}
        response = requests.get(endpoint, params=params)
        data_4h = response.json()
        params = {"symbol": coin_name, "interval": interval_3, "limit": limit4}
        response = requests.get(endpoint, params=params)
        data_1h = response.json()
        params = {"symbol": coin_name, "interval": interval_4, "limit": limit5}
        response = requests.get(endpoint, params=params)
        data_15m = response.json()

        df_data, styled_df, ana_df = hour_data(data, coin_name)
        df_data_1d, styled_df_1d, ana_df_1d = hour_data(data_1d, coin_name)
        df_data_4h, styled_df_4h, ana_df_4h = hour_data(data_4h, coin_name)
        df_data_1h, styled_df_1h, ana_df_1h = hour_data(data_1h, coin_name)
        df_data_15m, styled_df_15m, ana_df_15m = hour_data(data_15m, coin_name)

        print(ana_df)

        # # print(styled_df)
        # # print(df_data)
        # st.write("##LAST 15 DAYS DATA")
        # st.dataframe(styled_df)
        # fig = go.Figure(data=[go.Candlestick(x=ana_df['Open Time'],
        #                                      open=ana_df['Open'],
        #                                      high=ana_df['High'],
        #                                      low=ana_df['Low'],
        #                                      close=ana_df['Close'])])
        # st.plotly_chart(fig, use_container_width=True)
        # st.write("##LAST 15 4H DATA")
        # fig1 = go.Figure(data=[go.Candlestick(x=ana_df_4h['Open Time'],
        #                                       open=ana_df_4h['Open'],
        #                                       high=ana_df_4h['High'],
        #                                       low=ana_df_4h['Low'],
        #                                       close=ana_df_4h['Close'])])
        # st.plotly_chart(fig1, use_container_width=True)
        # st.write("##LAST 15 1H DATA")
        # fig2 = go.Figure(data=[go.Candlestick(x=ana_df_1h['Open Time'],
        #                                       open=ana_df_1h['Open'],
        #                                       high=ana_df_1h['High'],
        #                                       low=ana_df_1h['Low'],
        #                                       close=ana_df_1h['Close'])])
        # st.plotly_chart(fig2, use_container_width=True)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def hour_data(data, coin_name):
    ana_df = pd.DataFrame(data, columns=["Open Time", "Open", "High", "Low", "Close", "Volume", "Close Time",
                                         "Quote Asset Volume", "Number of Trades", "Taker Buy Base Asset Volume",
                                         "Taker Buy Quote Asset Volume", "Ignore"])

    ana_df["Open Time"] = ana_df["Open Time"].apply(lambda x: pd.to_datetime(float(
        x), unit='ms') if is_number(x) else pd.to_datetime(x, format='%Y-%m-%d %H:%M:%S.%f'))
    ana_df["Close"] = pd.to_numeric(ana_df["Close"])
    # Calculate rate of change for each day
    column_name = f"{coin_name}"
    ana_df[column_name] = ana_df['Close'].pct_change() * 100

    df_data = ana_df[[column_name, "Open Time"]]
    df_data = pd.DataFrame(df_data)
    df_data.set_index("Open Time", inplace=True)
    df_data = pd.DataFrame(df_data).transpose()

    last_10_columns = df_data.iloc[:, -10:]

    styled_df = last_10_columns.style.applymap(
        lambda x: 'color: red' if x < 0 else 'color: green')
    return df_data, styled_df, ana_df

    # Append to the combined DataFrame


interval = "1d"
limit = 10
# Define the API endpoint

previous_day_df = get_data()

df_combined = pd.DataFrame()

if not path.exists("multiday_data.csv"):
    print("previous_data_not_found:")
    tickers = partha_account.futures_ticker()
    column_name_df = pd.DataFrame(tickers)
    column_name_df = column_name_df[column_name_df['symbol'].str.endswith(
        'USDT')]

    symbols = column_name_df['symbol'].tolist()
    # symbols = usdt_list
    data1 = 0

    for symbol in symbols:
        # Construct the API request URL
        params = {"symbol": symbol, "interval": interval, "limit": limit}
        response = requests.get(endpoint, params=params)
        data = response.json()
        # print(data)
        data1 += 1
        progress = f"getting data : {data1} / {len(symbols)}"
        print(progress, end="\r")

        # Convert the data to a DataFrame
        df = pd.DataFrame(data, columns=["Open Time", "Open", "High", "Low", "Close", "Volume", "Close Time",
                                         "Quote Asset Volume", "Number of Trades", "Taker Buy Base Asset Volume",
                                         "Taker Buy Quote Asset Volume", "Ignore"])
        df["Open Time"] = pd.to_datetime(df["Open Time"], unit="ms").dt.date
        df["Close"] = pd.to_numeric(df["Close"])

        # Calculate rate of change for each day
        column_name = f"{symbol}"
        df[column_name] = df['Close'].pct_change() * 100

        # Append to the combined DataFrame
        df_combined = pd.concat([df_combined, df[[column_name]]], axis=1)

    df_combined.to_csv("multiday_data.csv")
    time.sleep(1)

else:
    print("previous_data_found:")
    df_combined = pd.read_csv("multiday_data.csv")

# Create a dictionary to map page names to their respective functions
pages = {
    "Page 1": Today_data,
    "Page 2": chart_data
}

# Create a selectbox to choose the page
selected_page = st.sidebar.selectbox(
    "Select a page", list(pages.keys()))

# Call the selected page function
pages[selected_page]()
