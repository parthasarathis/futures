
from binance.client import Client
from binance.enums import *
import time

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


# Get user input
symbol = input("Enter the trading symbol to use (e.g. BTCUSDT): ")
amount = float(
    input("Enter the amount to buy in COINS (e.g. 100): "))
leverage = int(input("Enter the leverage to set: "))
trailing_percentage = float(
    input("Enter the trailing stop loss percentage (default: 0.5): "))

# Calculate order parameters
ticker = partha_account.futures_symbol_ticker(symbol=symbol)
partha_account.futures_change_leverage(leverage=leverage, symbol=symbol)
market_price = float(ticker['price'])

# Place a long order
order = partha_account.futures_create_order(
    symbol=symbol,
    side=SIDE_BUY,
    type=FUTURE_ORDER_TYPE_MARKET,
    positionSide="LONG",
    quantity=amount,
)
print('Long order placed: \n')

entry_price = get_position()
stop_price = float(entry_price) * (1 - trailing_percentage / 100)

# Start monitoring the price and adjusting the stop price
while True:
    # Get the current market price
    ticker = partha_account.futures_symbol_ticker(symbol=symbol)
    market_price = float(ticker['price'])
    trail_price = float(market_price) * (1 - trailing_percentage / 100)
    current_pnl = (((market_price / float(entry_price)) - 1) * leverage)
    fixed_pnl = (((float(stop_price) / float(entry_price)) - 1) * leverage)
    print("SP = {:12.7f} : pnl = {:12.7f} : fpnl :{:12.7f}".format(
        stop_price, current_pnl, fixed_pnl), end="\r")

    if current_pnl >= float(leverage):
        trailing_percentage = 1

    # If the trailing stop price is higher than the current stop price, update the stop price
    if trail_price > float(stop_price):
        stop_price = trail_price

    # If the market price drops below the stop price, sell all the order
    if (market_price < float(stop_price)) or current_pnl > 100:
        order = partha_account.futures_create_order(
            symbol=symbol,
            side=SIDE_SELL,
            type=FUTURE_ORDER_TYPE_MARKET,
            positionSide="LONG",
            quantity=amount,
        )
        print('Market sell order placed:', order)

        # Calculate and print the PNL
        entry_value = float(entry_price) * amount
        exit_value = float(order['price']) * amount
        pnl = exit_value - entry_value
        print('PNL:', pnl)

        break

    # Wait for 3 seconds before checking the price again

    time.sleep(3)
