import ccxt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time


def plot_order_book_histogram(order_book, current_price, max_bid_quantity, max_bid_price, max_ask_quantity, max_ask_price):

    bids = order_book['bids']
    asks = order_book['asks']

    bids = order_book['bids']
    bid_prices = [float(bid[0]) for bid in bids]
    bid_quantities = [float(bid[1]) for bid in bids]
    bid_cumulative_sum = [sum(bid_quantities[:i + 1])
                          for i in range(len(bid_quantities))]

    asks = order_book['asks']
    ask_prices = [float(ask[0]) for ask in asks]
    ask_quantities = [float(ask[1]) for ask in asks]
    ask_cumulative_sum = [sum(ask_quantities[:i + 1])
                          for i in range(len(ask_quantities))]

    bid_prices, bid_quantities = zip(*bids)
    ask_prices, ask_quantities = zip(*asks)
    plt.clf()
    fig, ax1 = plt.subplots()
    ax1.plot(bid_prices, bid_quantities, color='b', linestyle='-',
             linewidth=2, label='Cumulative Bid Quantity')
    ax1.plot(ask_prices, ask_quantities, color='r', linestyle='-',
             linewidth=2, label='Cumulative Ask Quantity')

    ax2 = ax1.twinx()  # Create a second y-axis on the right side
    ax2.hist(bid_prices, bins=100, weights=bid_quantities, color='g',
             alpha=0.7, label='Bids', orientation='horizontal')
    ax2.hist(ask_prices, bins=100, weights=ask_quantities, color='r',
             alpha=0.7, label='Asks', orientation='horizontal')
    ax2.axhline(y=max_ask_price, color='red',
                linestyle='--', label='Max Bid Quantity')
    ax2.axhline(y=max_bid_price, color='green',
                linestyle='--', label='Max Ask Quantity')
    ax2.axhline(y=current_price, color='b',
                linestyle='--', label='Current Price')
    plt.text(1.3, 1.35, f"Resistance: {max_ask_price:.6f}", ha='right', va='top', transform=plt.gca().transAxes, color='red',
             fontsize=8, bbox=dict(facecolor='white', alpha=0.5))
    plt.text(1.3, 1.25, f"Current Price: {current_price:.6f}", ha='right', va='top', transform=plt.gca().transAxes, color='Black',
             fontsize=8, bbox=dict(facecolor='white', alpha=0.5))
    plt.text(1.3, 1.15, f"support: {max_bid_price:.6f}", ha='right', va='top', transform=plt.gca().transAxes, color='green',
             fontsize=8, bbox=dict(facecolor='white', alpha=0.5))
    ax2.xaxis.tick_top()
    ax2.invert_xaxis()

    ax1.set_xlabel('Quantity')
    ax1.set_ylabel('Price')
    ax1.set_title('Binance Futures Order Book')
    ax1.legend(loc='upper left')
    ax1.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()

    #  # Clear the previous plot
    # plt.hist(bid_prices, bins=100, weights=bid_quantities, color='g', alpha=0.7, label='Bids', orientation='horizontal')
    # plt.hist(ask_prices, bins=100, weights=ask_quantities, color='r', alpha=0.7, label='Asks', orientation='horizontal')
    # plt.axhline(y=max_ask_price, color='red', linestyle='--', label='Max Bid Quantity')
    # plt.axhline(y=max_bid_price, color='green', linestyle='--', label='Max Ask Quantity')
    # plt.axhline(y=current_price, color='b', linestyle='--', label='Current Price')

    # plt.text(0.95, 0.95, f"Resistance: {max_ask_price:.6f}", ha='right', va='top', transform=plt.gca().transAxes,color ='red',
    #          fontsize=8, bbox=dict(facecolor='white', alpha=0.5))
    # plt.text(0.95, 0.90, f"Current Price: {current_price:.6f}", ha='right', va='top', transform=plt.gca().transAxes,color ='Black',
    #          fontsize=8, bbox=dict(facecolor='white', alpha=0.5))
    # plt.text(0.95, 0.85, f"support: {max_bid_price:.6f}", ha='right', va='top', transform=plt.gca().transAxes,color ='green',
    #          fontsize=8, bbox=dict(facecolor='white', alpha=0.5))

    # plt.plot(bid_cumulative_sum, bid_prices, color='b', linestyle='-', linewidth=2, label='Cumulative Bid Quantity')
    # plt.plot(ask_cumulative_sum, ask_prices, color='r', linestyle='-', linewidth=2, label='Cumulative Ask Quantity')

    # plt.xlabel('Quantity')
    # plt.ylabel('Price')
    # plt.title('Binance Futures Order Book')
    # plt.legend(loc='lower right')
    # plt.grid(axis='x', linestyle='--', alpha=0.7)
    # plt.tight_layout()


def fetch_binance_futures_order_book(symbol, limit):
    exchange = ccxt.binance({
        'rateLimit': 4000,
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


def update_plot():
    try:
        order_book = fetch_binance_futures_order_book(symbol, limit)
        current_price = fetch_current_price(symbol=symbol)
        max_bid_quantity, max_bid_price = fetch_max_bid(order_book)
        max_ask_quantity, max_ask_price = fetch_max_ask(order_book)
        plot_order_book_histogram(
            order_book, current_price, max_bid_quantity, max_bid_price, max_ask_quantity, max_ask_price)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    symbol = 'SUI/USDT'
    limit = 100
    plt.figure(figsize=(10, 6))
    # Update plot every 5 seconds
    update_plot()
    plt.show()
