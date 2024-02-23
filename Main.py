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
TERMINAL_WIDTH = 100
PAGE = "home"
COMMAND_LIST = ["exit", "close", "equity"]
EQUITY_COMMAND_LIST = ["exit", "des", "stat", "cn", "gp", "gip", "dvd", "ern", "fa"]

#Initalize Instances
equity_instance = Equity("")


def interpret_command(command: list) -> str:
    """Checks if command is valid

    Args:
        command (str): command line input

    Returns:
        Str: Returns 'valid' if command is valid otherwise returns formatted invalid message
    """
    global PAGE
    match PAGE:
        case "home":
            if command[0] in COMMAND_LIST:
                return 'valid'
            else:
                return f'{f'Invalid Command: {command[0]}':^{TERMINAL_WIDTH - 4}}'
        case "equity":
            if command[0] in EQUITY_COMMAND_LIST:
                return 'valid'
            else:
                return f'{f'Invalid Command: {command[0]}':^{TERMINAL_WIDTH - 4}}'
        case _:
            return (f'{f'Unexpected Exception interpret_command -> match PAGE':^{TERMINAL_WIDTH - 4}}')
        

def execute_command(command: list) -> list:
    """Executes commands from CLI with seperate method calls

    Args:
        command (list): list of command arguments

    Returns:
        list: row_data[] from executing given ncommand
    """
    global PAGE
    match PAGE:
        case "home":
            match command[0]:
                case "equity":
                    PAGE = "equity"
                    return equity_instance.equity_command(command, TERMINAL_WIDTH)
                case "exit":
                    return Exit.exit_command(TERMINAL_WIDTH)
                case "close":
                    exit()
                case _:
                    return (['Unexpected Exception execute_command -> match PAGE -> case "home" -> match command[0]'])
        case "equity":
            match command[0]:
                case "exit":
                    PAGE = "home"
                    return Exit.exit_command(TERMINAL_WIDTH)
                case "des":
                    return equity_instance.equity_command_des(TERMINAL_WIDTH)
                case "stat":
                    return equity_instance.equity_command_stat(TERMINAL_WIDTH)
                case "cn":
                    return equity_instance.equity_command_cn(TERMINAL_WIDTH)
                case "gp":
                    return equity_instance.equity_command_gp(TERMINAL_WIDTH)
                case"gip":
                    return equity_instance.equity_command_gip(TERMINAL_WIDTH)
                case "dvd":
                    return equity_instance.equity_command_dvd(TERMINAL_WIDTH)
                case "ern":
                    return equity_instance.equity_command_ern(TERMINAL_WIDTH)
                case "fa":
                    return equity_instance.equity_command_fa(TERMINAL_WIDTH)
                case _:
                    return (['Unexpected Exception execute_command -> match PAGE -> case "equity" -> match command[0]'])
                    
 

                   
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