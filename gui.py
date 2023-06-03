import PySimpleGUI as sg
import threading
from binance.client import Client

# Binance API credentials
api_key = "<your-api-key>"
sec_key = "<your-secret-key>"

# Create a Binance client
client = Client(api_key, sec_key)

# Function to fetch Binance values


def fetch_binance_values(window):
    while True:
        try:
            # Get the current bitcoin value
            ticker = client.get_symbol_ticker(symbol='BTCUSDT')
            bitcoin_value = ticker['price']

            # Update the GUI window with the bitcoin value
            window.Element('bitcoin_value').Update(bitcoin_value)
        except Exception as e:
            print("Error:", str(e))

        # Sleep for 5 seconds before fetching again
        threading.Timer(5, fetch_binance_values, args=[window]).start()


# Create the layout for the GUI
layout = [
    [sg.Text('Bitcoin Value: '), sg.Text(size=(10, 1), key='bitcoin_value')],
    [sg.Button('Exit')]
]

# Create the GUI window
window = sg.Window('Binance Values', layout, finalize=True)

# Start fetching Binance values in a separate thread
threading.Thread(target=fetch_binance_values, args=[window]).start()

# Event loop to process GUI events
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break

# Close the GUI window
window.Close()
