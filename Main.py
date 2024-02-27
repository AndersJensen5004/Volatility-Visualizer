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

# Initalize Instances
equity_instance = Equity("")


def invalid_command(command: list, TERMINAL_WIDTH: int) -> list:
    row_data = []
    row_data.extend(["*" + " " * (TERMINAL_WIDTH - 6) + "*" for _ in range(5)])
    row_data.append(f'{f"Invalid Command >>> {command[0]}" :^{TERMINAL_WIDTH - 4}}')
    row_data.extend(["*" + " " * (TERMINAL_WIDTH - 6) + "*" for _ in range(5)])
    return row_data


def execute_command(command: list) -> list:
    """Executes commands from CLI with seperate method calls

    Args:
        command (list): list of command arguments

    Returns:
        list: row_data[] from executing given ncommand
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


def print_logo() -> None:
    print("▄▄███▄▄·██╗   ██╗ ██████╗ ██╗     \n" +
          "██╔█═══╝██║   ██║██╔═══██╗██║     \n" +
          "███████╗██║   ██║██║   ██║██║     \n" +
          "╚══█═██║╚██╗ ██╔╝██║   ██║██║     \n" +
          "███████║ ╚████╔╝ ╚██████╔╝███████╗\n" +
          "╚═▀▀▀══╝  ╚═══╝   ╚═════╝ ╚══════╝\n"
          )
    time.sleep(0.1)


def window_main(row_data):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("╔" + ("═" * (TERMINAL_WIDTH - 2)) + "╗")
    for set in row_data:
        print("║ ", end="")
        print(set, end="")
        print(" ║")
    print("╚" + ("═" * (TERMINAL_WIDTH - 2)) + "╝")


def command_line(w):
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
            command_list.append(chr(key))
            w.addstr(cursor_y, cursor_x + 1, chr(key), curses.color_pair(2))
            cursor_x += 1
            w.refresh()
            w.move(cursor_y, cursor_x + 1)
    # Join command
    return ''.join(command_list)


def main():
    ## Commands
    # print_logo()
    # row_data = []
    # for i in range(0, 5):
    #    row_data.append(("*" + " "*(TERMINAL_WIDTH - 6) +"*"))
    # row_data.append(("COMMANDS:" + " "*(TERMINAL_WIDTH - 14) +"*"))
    # row_data.append(("close - closes terminal" + " "*(TERMINAL_WIDTH - 28) +"*"))
    # row_data.append(("exit - return to home (this page)" + " "*(TERMINAL_WIDTH - 38) +"*"))
    # row_data.append(("equity <symbol> - loads equity" + " "*(TERMINAL_WIDTH - 35) +"*"))
    # for i in range(0, 5):
    #    row_data.append(("*" + " "*(TERMINAL_WIDTH - 6) +"*"))

    # while True:
    #    window_main(row_data)
    #    command = input(">>> ").lower().split(" ")
    #    row_data = execute_command(command)
    # Setup curses
    stdscr = curses.initscr()
    curses.cbreak()
    stdscr.keypad(True)

    # Define window size and position
    height, width = stdscr.getmaxyx()
    window_height = height  # Adjust for window border
    window_width = width  # Adjust for window border

    # Create window with border
    window = curses.newwin(window_height, window_width, 0, 0)
    window.border(9553, 9553, 9552, 9552, 9556, 9559, 9562, 9565)
    window.refresh()

    # Get user input
    command = command_line(window)

    # Restore terminal settings
    curses.echo()
    curses.nocbreak()
    stdscr.keypad(False)
    curses.endwin()

    # Return the command entered by the user
    return command


# Run
if __name__ == "__main__":
    command = main()
    print("Command entered:", command)

    # except KeyboardInterrupt:
    #    pass
