# Imports
import pandas as pd
import numpy as np
import os
import sys
import time
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta
# Class Imports
from equity.equity import Equity

# Initialize terminal
TERMINAL_WIDTH = 100
COMMAND_LIST = ["exit", "close", "equity"]
PAGE = "home"


def interpret_command(command: list) -> str:
    """Checks if command is valid

    Args:
        command (str): command line input

    Returns:
        Str: Returns 'valid' if command is valid otherwise returns formatted invalid message
    """
    if command[0] in COMMAND_LIST:
        return 'valid'
    else:
        return f'{f'Invalid Command: {command[0]}':^{TERMINAL_WIDTH - 4}}'
        

def execute_command(command: list) -> list:
    """Executes commands from CLI with seperate method calls

    Args:
        command (list): list of command arguments

    Returns:
        list: row_data[] from executing given ncommand
    """
    match command[0]:
        case "equity":
            PAGE = "equity"
            return Equity.equity_command(command, TERMINAL_WIDTH)
        case "exit":
            PAGE = "home"
            return exit_command(command)
        case "close":
            exit()
        case _:
            return (f'{f'Unexpected Exception':^{TERMINAL_WIDTH - 4}}')
                    
 
def exit_command(command: list) -> list:
    row_data = []
    for i in range(0, 5):
        row_data.append(("*" + " "*(TERMINAL_WIDTH - 6) +"*"))
    row_data.append(("COMMANDS:" + " "*(TERMINAL_WIDTH - 14) +"*"))
    row_data.append(("close - closes terminal" + " "*(TERMINAL_WIDTH - 28) +"*"))
    row_data.append(("exit - return to home (this page)" + " "*(TERMINAL_WIDTH - 38) +"*"))
    row_data.append(("equity <symbol> - loads equity" + " "*(TERMINAL_WIDTH - 35) +"*"))
    for i in range(0, 5):
        row_data.append(("*" + " "*(TERMINAL_WIDTH - 6) +"*"))
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
        output = interpret_command(command)
        if(output != "valid"):
            row_data[0] = output
        else:
            row_data = execute_command(command)

# Run
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass