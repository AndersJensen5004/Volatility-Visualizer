# Imports
import os
import time
import matplotlib.pyplot as plt
import yfinance as yf
import curses
from curses import *
# Class Imports
from equity import *
from exit.exit import Exit

# Initialize terminal
TERMINAL_WIDTH = 150
PAGE = "home" # remove shit global variables

#Initalize Instances
equity_instance = Equity("")

        
def invalid_command(command: list, TERMINAL_WIDTH: int) -> list:
    row_data = []
    row_data.extend(["*" + " " * (TERMINAL_WIDTH - 6) + "*" for _ in range(5)])
    row_data.append(f'{f'Invalid Command >>> {command[0]}':^{TERMINAL_WIDTH - 4}}')
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

    current_page_commands = command_mappings.get(PAGE, command_mappings["home"]) #home is default page
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
    print(Style.RESET_ALL)
    time.sleep(0.1)  

def window_main(row_data):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("╔"+("═"*(TERMINAL_WIDTH - 2))+"╗")
    for set in row_data:
        print("║ ", end="")
        print(set, end="")
        print(" ║")   
    print("╚"+("═"*(TERMINAL_WIDTH - 2))+"╝")
    
    
def main(stdscr):
   ## Commands
   #print_logo()
   #row_data = []
   #for i in range(0, 5):
   #    row_data.append(("*" + " "*(TERMINAL_WIDTH - 6) +"*"))
   #row_data.append(("COMMANDS:" + " "*(TERMINAL_WIDTH - 14) +"*"))
   #row_data.append(("close - closes terminal" + " "*(TERMINAL_WIDTH - 28) +"*"))
   #row_data.append(("exit - return to home (this page)" + " "*(TERMINAL_WIDTH - 38) +"*"))
   #row_data.append(("equity <symbol> - loads equity" + " "*(TERMINAL_WIDTH - 35) +"*"))
   #for i in range(0, 5):
   #    row_data.append(("*" + " "*(TERMINAL_WIDTH - 6) +"*"))

   #while True:
   #    window_main(row_data)
   #    command = input(">>> ").lower().split(" ")
   #    row_data = execute_command(command)
    # Initialize curses
    # Initialize curses
    curses.curs_set(0)  # Hide the cursor

    # Get the size of the terminal window
    height, width = stdscr.getmaxyx()

    # Create a textbox at the top for user input
    input_box = curses.newwin(3, width, 0, 0)
    input_box.addstr(1, 1, ">>> ")
    input_box.refresh()

    # Main loop
    while True:
        # Get user input
        user_input = input_box.getstr(1, 5, width - 5).decode("utf-8")

        # Handle user input (process command)
        # For now, we just print the input
        stdscr.addstr(5, 0, f"Command: {user_input}")
        stdscr.refresh()

        # Clear input box
        input_box.clear()
        input_box.addstr(1, 1, ">>> ")
        input_box.refresh()
        
# Run
if __name__ == "__main__":
    #try:
    curses.wrapper(main)
   
    #except KeyboardInterrupt:
    #    pass