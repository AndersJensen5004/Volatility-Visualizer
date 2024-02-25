import yfinance as yf

ticker = yf.Ticker("NVDA")
info = ticker.info
print("-"*55)
print(info)
print("-"*55)

import curses
from curses import wrapper

def main(stdscr):
    stdscr.clear()
    stdscr.refresh()
    stdscr.getch()
    
    pass


wrapper(main)
