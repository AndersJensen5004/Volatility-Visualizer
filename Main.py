# Imports
import pandas as pd
import numpy as np
import os
import time
import matplotlib.pyplot as plt
import yfinance as yf
# Class Imports
from equity import *
from exit.exit import Exit

# Initialize terminal
TERMINAL_WIDTH = 150
PAGE = "home"
COMMAND_LIST = ["exit", "close", "equity"]
EQUITY_COMMAND_LIST = ["exit", "des", "stat", "cn", "gp", "gip", "dvd", "ern", "fa"]

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
    time.sleep(0.1)  

def window_main(row_data):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("╔"+("═"*(TERMINAL_WIDTH - 2))+"╗")
    for set in row_data:
        print("║ ", end="")
        print(set, end="")
        print(" ║")   
    print("╚"+("═"*(TERMINAL_WIDTH - 2))+"╝")
    
    
def main() -> None:
    # Commands
    print_logo()
    row_data = []
    for i in range(0, 5):
        row_data.append(("*" + " "*(TERMINAL_WIDTH - 6) +"*"))
    row_data.append(("COMMANDS:" + " "*(TERMINAL_WIDTH - 14) +"*"))
    row_data.append(("close - closes terminal" + " "*(TERMINAL_WIDTH - 28) +"*"))
    row_data.append(("exit - return to home (this page)" + " "*(TERMINAL_WIDTH - 38) +"*"))
    row_data.append(("equity <symbol> - loads equity" + " "*(TERMINAL_WIDTH - 35) +"*"))
    for i in range(0, 5):
        row_data.append(("*" + " "*(TERMINAL_WIDTH - 6) +"*"))

    while True:
        window_main(row_data)
        command = input(">>> ").lower().split(" ")
        row_data = execute_command(command)
        
# Run
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass