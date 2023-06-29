import time
from binance.client import Client

# Replace with your Binance API keys
api_key = "FLPeS5t9QAntmcsEtYYv01JBZufM5SQQu751qh0s9rcHwVXZqioztxpMnyVMxvlP"
sec_key = "kP7twDqEL7alJGf4R4uDH6cNsivpscabZ4EEdD9SWJugC7DOJu7YHfcgeP8ngUJw"
# Create a Binance client
client = Client(api_key, sec_key)

# Retrieve the order book data
symbol = 'BTCUSDT'  # Replace with the desired trading pair

# Function to print the bar graph
def print_bar_graph(bids, asks):
    max_quantity = max(max(bids), max(asks))
    bar_width = 50

    # Clear the terminal
    print("\033c", end="")

    # Print the bids
    print("Bids:")
    for price, quantity in zip(bids, asks):
        quantity_str = int(quantity)
        print(f"{price:<15} | {'#' * quantity_str}")

    print("\n")

    # Print the asks
    print("Asks:")
    for price, quantity in zip(bids, asks):
        quantity_str = int(quantity)
        print(f"{price:<15} | {'#' * quantity_str}")

    print("\n")

while True:
    # Retrieve the order book data
    order_book = client.get_order_book(symbol=symbol)

    # Extract the prices and quantities from the order book
    bids = [float(bid[0]) for bid in order_book['bids']]
    quantities_bids = [float(bid[1]) for bid in order_book['bids']]

    asks = [float(ask[0]) for ask in order_book['asks']]
    quantities_asks = [float(ask[1]) for ask in order_book['asks']]

    # Print the bar graph
    print_bar_graph(bids, asks)

    # Delay for 3 seconds
    time.sleep(3)
