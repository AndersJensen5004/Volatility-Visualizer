#TEST COMMITt
# Imports
import os
import time
import curses
from curses import *
# Class Imports
from equity import *
from exit.exit import Exit

# Initialize terminal
TERMINAL_WIDTH = 150
PAGE = "home"  # remove shit global variables

# Initialize Instances
equity_instance = Equity("")


def invalid_command(w, command: list) -> None:
    """
    Prints out invalid command in terminal

    Args:
        w: curses window
        command (list): list of command arguments

    Returns: Nothing

    """
    w.refresh()
    w.addstr(1, 3, f"Invalid Command >>> {command[0]}")

def execute_command(command: list) -> list:
    """Executes commands from CLI with separate method calls

    Args:
        command (list): list of command arguments

    Returns:
        list: row_data[] from executing given command
    """

    global PAGE
    command_mappings = {
        "home": {
            "equity": lambda: ("equity", equity_instance.equity_command(command, TERMINAL_WIDTH)),
            "exit": lambda: ("home", Exit.exit_command(TERMINAL_WIDTH)),
            "close": lambda: ("exit", exit()),
            "_default": lambda: ("home", invalid_command(command, TERMINAL_WIDTH)),
        },
        "equity": {
            "exit": lambda: ("home", Exit.exit_command(TERMINAL_WIDTH)),
            "equity": lambda: ("equity", equity_instance.equity_command(command, TERMINAL_WIDTH)),
            "des": lambda: ("equity", equity_instance.equity_command_des(TERMINAL_WIDTH)),
            "stat": lambda: ("equity", equity_instance.equity_command_stat(TERMINAL_WIDTH)),
            "cn": lambda: ("equity", equity_instance.equity_command_cn(TERMINAL_WIDTH)),
            "gp": lambda: ("equity", equity_instance.equity_command_gp(TERMINAL_WIDTH)),
            "gip": lambda: ("equity", equity_instance.equity_command_gip(TERMINAL_WIDTH)),
            "dvd": lambda: ("equity", equity_instance.equity_command_dvd(TERMINAL_WIDTH)),
            "ern": lambda: ("equity", equity_instance.equity_command_ern(TERMINAL_WIDTH)),
            "fa": lambda: ("equity", equity_instance.equity_command_fa(TERMINAL_WIDTH)),
            "_default": lambda: ("equity", invalid_command(command, TERMINAL_WIDTH)),
        }
    }

    current_page_commands = command_mappings.get(PAGE, command_mappings["home"])  # home is default page
    command_function = current_page_commands.get(command[0], current_page_commands["_default"])

    # Execute
    PAGE, row_data = command_function()
    return row_data


def window_main(row_data):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("╔" + ("═" * (TERMINAL_WIDTH - 2)) + "╗")
    for set in row_data:
        print("║ ", end="")
        print(set, end="")
        print(" ║")
    print("╚" + ("═" * (TERMINAL_WIDTH - 2)) + "╝")


def command_line(w, w_width: int) -> list:
    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    # Don't echo user's keystrokes
    curses.noecho()
    # Enable keypad mode for special keys
    w.keypad(True)

    # Initialize the command string
    command_list = []
    cursor_x = 4  # Adjust cursor position
    cursor_y = 1

    # Print a prompt
    w.refresh()
    w.addstr(1, 1, ">>> ", curses.color_pair(1))  # Adjust position
    w.refresh()

    while True:
        # Get user input
        key = w.getch()
        # Handling special keys
        if key == curses.KEY_ENTER or key in [10, 13]:
            break
        # IN WINDOWS11 IT'S 8 I DON'T KNOW WHAT THE OTHER NUMBERS ARE
        elif key == curses.KEY_BACKSPACE or key == 127 or key == 22 or key == 8:
            if len(command_list) > 0:  # Adjust position
                command_list.pop()
                cursor_x -= 1
                w.addstr(cursor_y, cursor_x + 1, " ")  # Clear character
                w.refresh()
                w.move(cursor_y, cursor_x + 1)
        elif 32 <= key <= 126:  # Printable characters
            if len(command_list) < (w_width - 8):  # Not allowing user to overflow window
                command_list.append(chr(key))
                w.addstr(cursor_y, cursor_x + 1, chr(key), curses.color_pair(2))
                cursor_x += 1
                w.refresh()
                w.move(cursor_y, cursor_x + 1)

    # join commands and split them into a list of lowercase arguments
    commands = (''.join(command_list)).lower().split(' ')
    command_list = []
    for c in commands:
        if c != '':
            command_list.append(c)
    return command_list


def main():
    stdscr = curses.initscr()
    curses.cbreak()
    stdscr.keypad(True)

    # Define window size and position
    window_height, window_width = stdscr.getmaxyx()

    # Create window with border
    main_window = curses.newwin(window_height, window_width, 0, 0)
    main_window.border(9553, 9553, 9552, 9552, 9556, 9559, 9562, 9565)
    main_window.refresh()

    # Get user input
    while True:
        user_command = command_line(main_window, window_width)
        execute_command(user_command)
        main_window.refresh()

        # Restore terminal settings
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

    # except KeyboardInterrupt:
    #    pass
