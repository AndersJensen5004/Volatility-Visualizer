#import yfinance as yf

#ticker = yf.Ticker("NVDA")
#info = ticker.info
#print("-"*55)
#print(info)
#print("-"*55)

import curses


import curses

def main(stdscr):
    # Set up curses
    curses.curs_set(0)  # Hide the cursor
    stdscr.timeout(100)  # Set getch() timeout to 100 milliseconds

    # Create a pad
    pad = curses.newpad(100, 100)
    pad_pos = 0  # Initial position of the pad

    # Fill pad with content
    for i in range(100):
        pad.addstr(i, 0, f"Line {i}")

    while True:
        key = stdscr.getch()

        # Scroll up
        if key == curses.KEY_UP:
            pad_pos = max(0, pad_pos - 1)

        # Scroll down
        elif key == curses.KEY_DOWN:
            pad_pos = min(100 - curses.LINES, pad_pos + 1)

        # Quit on 'q' key press
        elif key == ord('q'):
            break

        # Clear the screen
        stdscr.clear()

        # Refresh the pad and the screen
        pad.refresh(pad_pos, 0, 0, 0, curses.LINES - 1, curses.COLS - 1)
        stdscr.refresh()

curses.wrapper(main)