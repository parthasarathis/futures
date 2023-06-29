import curses
import pandas as pd

data = {
    'Name': ['John', 'Alice', 'Bob'],
    'Age': [25, 28, 32],
    'City': ['New York', 'London', 'Paris']
}
df = pd.DataFrame(data)

stdscr = curses.initscr()
curses.noecho()
stdscr.keypad(True)
curses.cbreak()
curses.curs_set(0)

stdscr.clear()

df_string = df.to_string(index=False)

stdscr.addstr(0, 0, df_string)
stdscr.refresh()

stdscr.getch()

curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
