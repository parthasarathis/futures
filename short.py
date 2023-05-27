from binance.client import Client
from binance.enums import *
import time
import argparse


def prRed(skk):
    return "\033[91m {}\033[00m" .format(skk)


def prGreen(skk):
    return "\033[92m {}\033[00m" .format(skk)


def prYellow(skk):
    return "\033[93m {}\033[00m" .format(skk)


def prLightPurple(skk):
    return "\033[94m {}\033[00m" .format(skk)


def prPurple(skk):
    return "\033[95m {}\033[00m" .format(skk)


def prCyan(skk):
    return "\033[96m {}\033[00m" .format(skk)


def prLightGray(skk):
    return "\033[97m {}\033[00m" .format(skk)


def prBlack(skk):
    return "\033[98m {}\033[00m" .format(skk)


# Parse the command-line arguments
parser = argparse.ArgumentParser(
    description='Place a long order and follow the trailing stop loss.')
parser.add_argument('symbol', type=str,
                    help='The trading symbol to use (e.g. BTCUSDT)')
parser.add_argument('amount', type=float,
                    help='The amount to buy in the base asset (e.g. 0.1 for 0.1 BTC)')
parser.add_argument('leverage', type=int, help='leverage to set')
parser.add_argument(
    'tp', type=float, help='The trailing stop loss percentage (default: 0.5)')
args = parser.parse_args()

# Set up the client
api_key = "FLPeS5t9QAntmcsEtYYv01JBZufM5SQQu751qh0s9rcHwVXZqioztxpMnyVMxvlP"
sec_key = "kP7twDqEL7alJGf4R4uDH6cNsivpscabZ4EEdD9SWJugC7DOJu7YHfcgeP8ngUJw"
partha_account = Client(api_key=api_key, api_secret=sec_key)


futures_type = FuturesType.USD_M


def get_position():
    position = partha_account.futures_position_information(symbol=symbol)
    for p in position:
        if p['symbol'] == symbol and p['positionAmt'] != '0':
            print(p)
            return float(p['entryPrice'])


# Set the order parameters
symbol = args.symbol
amount_in_dollars = args.amount
# entry_price = str(args.entry_price)
trailing_percentage = args.tp

ticker = partha_account.futures_symbol_ticker(symbol=symbol)
market_price = float(ticker['price'])
amount = int(amount_in_dollars / market_price)


# Place a long order
order = partha_account.futures_create_order(
    symbol=symbol,
    side=SIDE_SELL,
    type=FUTURE_ORDER_TYPE_MARKET,
    positionSide="SHORT",
    quantity=amount,
)
print('Short order placed: \n')

entry_price = get_position()

stop_price = float(entry_price) * (1 + args.tp / 100)

# Start monitoring the price and adjusting the stop price
while True:
    # Get the current market price
    ticker = partha_account.futures_symbol_ticker(symbol=symbol)
    market_price = float(ticker['price'])
    trail_price = float(market_price) * (1 + args.tp / 100)
    print("pnl = {:10.4f} : fpnl :{:10.4f}".format((((entry_price/float(market_price))-1)
          * 50), (((float(entry_price)/float(stop_price))-1)*50)), end="\r")

    # Calculate the trailing stop price as a percentage of the entry price

    # If the trailing stop price is higher than the current stop price,
    # update the stop price
    if trail_price < float(stop_price):
        stop_price = trail_price
        # print('Stop loss updated to' + "{:10.4f}".format(stop_price) + "\n")

    # If the market price drops below the stop price, sell all the order
    if market_price > float(stop_price):
        order = partha_account.futures_create_order(
            symbol=symbol,
            side=SIDE_BUY,
            type=FUTURE_ORDER_TYPE_MARKET,
            positionSide="SHORT",
            quantity=amount,
        )
        print('Market sell order placed:', order)

        # Calculate and print the PNL
        entry_value = float(entry_price) * amount
        exit_value = float(order['price']) * amount
        pnl = exit_value - entry_value
        print('PNL:', pnl)

        break

    # Wait for 10 seconds before checking the price again
    time.sleep(3)
