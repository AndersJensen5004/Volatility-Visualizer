# Imports
import os
import time
import curses
import threading
from curses import *
# Class Imports
from equity import *
from exit.exit import Exit


# Initialize Instances
equity_instance = Equity(None)

PAD_Y: int = 0


def invalid_command(p, command: list) -> None:
    """
    Prints out invalid command in terminal

    Args:
        p: curses pad
        command (list): list of command arguments

    Returns: Nothing

    """
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    pad_height, pad_width = p.getmaxyx()
    message = f"Invalid Command >>> {command[0]}"
    message_length = len(message)

    start_y = 5
    start_x = max((pad_width - message_length) // 2, 2)

    p.addstr(start_y, start_x, message, curses.color_pair(4))


def execute_command(p, command: list) -> None:
    """Executes commands from CLI with separate method calls

    Args:
        p: curses pad
        command (list): list of command arguments

    """

    command_mappings = {
        "equity": lambda: (equity_instance.execute_command(p, command)),
        "close": lambda: (exit()),
        "_default": lambda: (invalid_command(p, command)),
    }

    command_function = command_mappings.get(command[0], command_mappings["_default"])

    # Execute
    command_function()


def draw_main(w) -> None:
    w.border(9553, 9553, 9552, 9552, 9556, 9559, 9562, 9565)
    w.refresh()


def command_line(w, p, window_height: int, window_width: int):
    global PAD_Y

    # Don't echo user's keystrokes
    curses.noecho()

    height, width = w.getmaxyx()
    pad_pos_y, pad_pos_x = 3, 1  # Position to display pad in main window

    # Enable keypad mode for special keys
    w.keypad(True)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)

    w.addstr(0, 0, ">>> ", curses.color_pair(1))  # CLI

    # Initialize the command string
    command_list = []
    cursor_x = 3  # Adjust cursor position
    cursor_y = 1
    cursor_y_offset = -1

    while True:
        # Get user input
        key = w.get_wch()
        try:
            key_value = ord(key)
        except TypeError:
            key_value = -1
        # Handling special keys
        if key == curses.KEY_ENTER or key_value in [10, 13]:
            break

        # IN WINDOWS IT'S 8 I DON'T KNOW WHAT THE OTHER NUMBERS ARE
        elif key == curses.KEY_BACKSPACE or key_value == 127 or key_value == 22 or key_value == 8:
            if len(command_list) > 0:  # Adjust position
                command_list.pop()
                cursor_x -= 1
                w.addch(cursor_y + cursor_y_offset, cursor_x + 1, " ")  # Clear character
                w.refresh()
                w.move(cursor_y + cursor_y_offset, cursor_x + 1)

        elif 32 <= key_value <= 126:  # Printable characters
            if len(command_list) < (width - 6):  # Not allowing user to overflow window
                command_list.append(chr(key_value))
                w.addch(cursor_y + cursor_y_offset, cursor_x + 1, chr(key_value))
                cursor_x += 1
                w.refresh()
                w.move(cursor_y + cursor_y_offset, cursor_x + 1)

        elif key == curses.KEY_DOWN:
            PAD_Y += 1
            p.touchwin()
            p.refresh(PAD_Y, 0, pad_pos_y, pad_pos_x, pad_pos_y + window_height - 5, pad_pos_x + window_width - 2)
            redraw_pad_with_color(p, pad_pos_y, pad_pos_x, window_height, window_width)


        elif key == curses.KEY_UP:
            if PAD_Y > 0:
                PAD_Y -= 1
                p.touchwin()
                p.refresh(PAD_Y, 0, pad_pos_y, pad_pos_x, pad_pos_y + window_height - 5, pad_pos_x + window_width - 2)
                redraw_pad_with_color(p, pad_pos_y, pad_pos_x, window_height, window_width)


        elif key == curses.KEY_MOUSE:
            _, x, y, _, bstate = curses.getmouse()
            if bstate & curses.BUTTON1_PRESSED:
                pass

    # join commands and split them into a list of lowercase arguments
    commands = (''.join(command_list)).lower().split(' ')
    command_list = [c for c in commands if c != '']
    return command_list if command_list else [""]


def loading_screen(p) -> None:
    # Get window dimensions
    height, width = p.getmaxyx()

    curses.start_color()
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # Define the cat ASCII art
    cat = [
        "                        _    ",
        "                       | \\   ",
        "                       | |   ",
        "                       | |   ",
        "  |\\                   | |   ",
        " /, ~\\                / /    ",
        "X     `-.....-------./ /     ",
        " ~-. ~  ~              |     ",
        "    \\             /    |     ",
        "     \\  /_     ___\\   /     ",
        "     | /\\ ~~~~~   \\ |      ",
        "     | | \\        || |      ",
        "     | |\\ \\       || )      ",
        "    (_/ (_/      ((_/"
    ]

    text = [
        " ______              ______               ",
        "|  ___|             |  ___|              ",
        "| |_ _   _ _ __ _ __| |____   _____ _ __ ",
        "|  _| | | | '__| '__|  __\\ \\ / / _ \\ '__|",
        "| | | |_| | |  | |  | |___\\ V /  __/ |   ",
        "\\_|  \\__,_|_|  |_|  \\____/ \\_/ \\___|_|   ",
        " ______ _                                ",
        " |  __|(_)                               ",
        " | |_   _ _ __   __ _ _ __   ___ ___     ",
        " |  _| | | '_ \\ / _` | '_ \\ / __/ _ \\    ",
        " | |   | | | | | (_| | | | | (_|  __/    ",
        " \\_|   |_|_| |_|\\__,_|_| |_|\\___\\___|    "
    ]

    # Calculate starting position for the cat to be centered
    # start_y_text = (height - len(text)) // 2
    start_y_text = 5
    start_x_text = 5
    # start_y_cat = (height - len(cat)) // 2
    start_y_cat = 5
    start_x_cat = int((width - len(cat[0])) // 1.5)

    # Print the text
    for i, line in enumerate(text):
        p.addstr(start_y_text + i, start_x_text, line, curses.color_pair(3))

    # Print the cat
    for i, line in enumerate(cat):
        p.addstr(start_y_cat + i, start_x_cat, line, curses.color_pair(3))



def main():
    stdscr = curses.initscr()
    curses.cbreak()
    stdscr.keypad(True)

    # Define window size and position
    window_height, window_width = stdscr.getmaxyx()

    # Create window with border
    main_window = curses.newwin(window_height, window_width, 0, 0)
    draw_main(main_window)

    # Create CLI window
    command_window = main_window.subwin(1, (window_width - 2), 1, 1)

    # Create pad
    pad_height = window_height - 5  # Height of pad (3 lines above and 2 lines below)
    pad_width = window_width - 2  # Width of pad (considering border)
    # pad = curses.newpad(pad_height, pad_width)
    pad = curses.newpad(1000, pad_width)  # Set initial height larger

    # Enable scrolling
    pad.scrollok(True)

    # Enable Mouse Inputs
    curses.mousemask(-1)
    curses.mouseinterval(0)

    # Creating Welcome Screen with Cat
    loading_screen(pad)
    pad_pos_y, pad_pos_x = 3, 1  # Position to display pad in main window
    pad.refresh(PAD_Y, 0, pad_pos_y, pad_pos_x, pad_pos_y + window_height - 5, pad_pos_x + window_width - 2)


    # Begin Curses color
    #

    # Get user input
    while True:
        user_command = command_line(command_window, pad, window_height, window_width)

        pad.clear()

        execute_command(pad, user_command)

        # Refresh entire pad in main window
        pad_pos_y, pad_pos_x = 3, 1  # Position to display pad in main window
        pad.refresh(PAD_Y, 0, pad_pos_y, pad_pos_x, pad_pos_y + window_height - 5, pad_pos_x + window_width - 2)

        command_window.clear()

        print(user_command)

    # Restore terminal settings
    curses.echo()
    curses.nocbreak()
    stdscr.keypad(False)
    curses.endwin()

    # Return the command entered by the user


# Run
if __name__ == "__main__":
    main()
