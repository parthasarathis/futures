import ccxt
import time
import pyfiglet
import schedule

def plot_order_book_histogram(order_book,current_price,max_bid_quantity,max_bid_price, max_ask_quantity,max_ask_price):
    bids = order_book['bids']
    asks = order_book['asks']

    bids = order_book['bids']
    bid_prices = [float(bid[0]) for bid in bids]
    bid_quantities = [float(bid[1]) for bid in bids]
    bid_cumulative_sum = [sum(bid_quantities[:i + 1]) for i in range(len(bid_quantities))]

    asks = order_book['asks']
    ask_prices = [float(ask[0]) for ask in asks]
    ask_quantities = [float(ask[1]) for ask in asks]
    ask_cumulative_sum = [sum(ask_quantities[:i + 1]) for i in range(len(ask_quantities))]

    bid_prices, bid_quantities = zip(*bids)
    ask_prices, ask_quantities = zip(*asks)


    print("\033c", end="")
    print(pyfiglet.figlet_format(f'Resis: {max_ask_price:.6f}',font = "slscript"))
    print(pyfiglet.figlet_format(f'CP: {current_price:.6f}',font = "slscript"))
    print(pyfiglet.figlet_format(f'Supp: {max_bid_price:.6f}',font = "slscript"))

def fetch_binance_futures_order_book(symbol, limit):
    exchange = ccxt.binance({
        'rateLimit': 1000,
        'enableRateLimit': True,
        'adjustForTimeDifference': True
    })

    order_book = exchange.fetch_order_book(symbol, limit)
    return order_book

def fetch_current_price(symbol):
    exchange = ccxt.binance({
        'rateLimit': 1000,
        'enableRateLimit': True,
        'adjustForTimeDifference': True
    })

    ticker = exchange.fetch_ticker(symbol)
    return ticker['last']

def fetch_max_bid(order_book):
    bids = order_book['bids']
    max_bid_quantity = max(float(bid[1]) for bid in bids)
    max_bid_price = None

    for bid in bids:
        if float(bid[1]) == max_bid_quantity:
            max_bid_price = float(bid[0])
            break

    return max_bid_quantity, max_bid_price

def fetch_max_ask(order_book):
    asks = order_book['asks']
    max_ask_quantity = max(float(ask[1]) for ask in asks)
    max_ask_price = None

    for ask in asks:
        if float(ask[1]) == max_ask_quantity:
            max_ask_price = float(ask[0])
            break
    return max_ask_quantity, max_ask_price


def update_plot(frame):
    try:
        order_book = fetch_binance_futures_order_book(symbol, limit)
        current_price = fetch_current_price(symbol=symbol)
        max_bid_quantity, max_bid_price = fetch_max_bid(order_book)
        max_ask_quantity, max_ask_price = fetch_max_ask(order_book)
        plot_order_book_histogram(order_book, current_price, max_bid_quantity, max_bid_price,max_ask_quantity,max_ask_price)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    symbol = 'XLM/USDT'
    limit = 5
    schedule.every(2).seconds.do(update_plot, frame=1)
    while(1):
        schedule.run_pending()