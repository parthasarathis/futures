import time

def print_table(data):
    # ANSI escape sequence to move the cursor to the beginning of the table
    print('\033[1;1H')
    for row in data:
        # Print each row of the table
        print(row)

# Example data
data = [
    ['John', 30],
    ['Alice', 25],
    ['Bob', 35]
]

# Update the table every 1 second
while True:
    print_table(data)
    # Wait for 1 second
    time.sleep(1)
    # ANSI escape sequence to clear the table content
    print('\033[2J')