# Imports
import pandas as pd
import numpy as np
import os
import sys
import time
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta
from tabulate import tabulate

# Initialize terminal
TERMINAL_WIDTH = 100
COMMAND_LIST = ["exit", "close", "equity"]


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
            return equity_command(command)
        case _:
            return f'{f'Unexpected Exception':^{TERMINAL_WIDTH - 4}}'
            
def equity_command(command: list) -> list:
    """Loads a symbol main menu for commands

    Args:
        command (list): _description_

    Returns:
        list: _description_
    """
    row_data = []
    if (len(command) != 2):
        return [(f'{f'Invalid Arguments -> Use equity <symbol>':^{TERMINAL_WIDTH - 4}}')]
    row_data.append(f'{f'<{command[1].upper()}>':^{TERMINAL_WIDTH - 4}}')
    row_data.append((" " * (TERMINAL_WIDTH - 4)))
    
    ticker = yf.Ticker(command[1])
    price = ticker.history(period='1d').iloc[-1].Close
    row_data.append(f'{f'${price:.4f}':^{TERMINAL_WIDTH - 4}}')
    return row_data

#    except Exception as e:
#        row_data.append(f'{f'<{type(e).__name__}> Exception':^{TERMINAL_WIDTH - 4}}')
#        row_data.append(f'{f'<{command[1].upper()}> is not a valid symbol.':^{TERMINAL_WIDTH - 4}}')
#        row_data.append((" " * (TERMINAL_WIDTH - 4)))
#        return row_data
                    
                    
def print_logo() -> None:
    print("▄▄███▄▄·██╗   ██╗ ██████╗ ██╗     \n" +
          "██╔█═══╝██║   ██║██╔═══██╗██║     \n" +
          "███████╗██║   ██║██║   ██║██║     \n" +
          "╚══█═██║╚██╗ ██╔╝██║   ██║██║     \n" +
          "███████║ ╚████╔╝ ╚██████╔╝███████╗\n" +
          "╚═▀▀▀══╝  ╚═══╝   ╚═════╝ ╚══════╝\n"
        )
    time.sleep(0.1)  
    


def third_friday_of_month(year: int, month: int) -> datetime:
    """Returns closest monthly Opex date

    Args:
        year (int): current year
        month (int): current month

    Returns:
        datetime: next montly Opex
    """
    first_day_of_month = datetime(year, month, 1)
    first_day_of_week = first_day_of_month.weekday()
    days_to_third_friday = (4 - first_day_of_week + 14) % 7
    third_friday = first_day_of_month + timedelta(days=days_to_third_friday)
    today = datetime.now()
    if third_friday < today:
        if month == 12:  
            return third_friday_of_month(year + 1, 1)
        else:
            return third_friday_of_month(year, month + 1)
    return third_friday

def get_options_chain() -> pd.DataFrame:
    """Get SPX options chain for nearest monthly Opex.

    Returns:
        pd.DataFrame: SPX options chain
    """
    spx = yf.Ticker("SPX")
    year = datetime.now().year
    month = datetime.now().month
    third_friday = third_friday_of_month(year, month)
    return spx.option_chain(third_friday)

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