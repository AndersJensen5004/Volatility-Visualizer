#import yfinance as yf

#ticker = yf.Ticker("NVDA")
#info = ticker.info
#print("-"*55)
#print(info)
#print("-"*55)

import curses


def draw_border(window):
    window.erase()
    window.border('|', 180, '-', '-', '+', '+', '+', '+')

    height, width = window.getmaxyx()
    title = "Test Application123123"
    window.addstr(0, max(1, width // 2 - len(title) // 2), title)
    window.refresh()  # Refresh the window to show the border


def main(stdscr):
    curses.curs_set(0)
    curses.noecho()
    stdscr.nodelay(True)

    draw_border(stdscr)
    while True:
        # curses.resize_term(10,10)
        key = stdscr.getch()
        if key == curses.KEY_RESIZE:
            draw_border(stdscr)
        elif key == ord('q'):
            curses.endwin()
            break


if __name__ == "__main__":
    print(ord("║"), ord("║"), ord("═"), ord("═"), ord("╔"), ord("╗"), ord("╚"), ord("╝"))
    curses.wrapper(main)