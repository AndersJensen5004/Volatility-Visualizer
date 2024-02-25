import yfinance as yf
from colorama import Fore, Back, Style

class Equity:
    
    def __init__(self, ticker):
        self.TICKER = ticker
        
    def equity_command(self, command: list, TERMINAL_WIDTH: int) -> list:
        """Loads a symbol main menu for commands

        Args:
            command (list): list of command arguments
            TERMINAL_WIDTH (int): width of terminal window

        Returns:
            list: row_data of command list for equity
        """
        
        margin = TERMINAL_WIDTH - 4
        color = 8
        reset = 7
        try:
            if (len(command) != 2):
                row_data = []
                row_data.extend(["*" + " " * (TERMINAL_WIDTH - 6) + "*" for _ in range(5)])
                row_data.append(f"{'Invalid Arguments -> Use equity <symbol>':^{margin}}")
                row_data.extend(["*" + " " * (TERMINAL_WIDTH - 6) + "*" for _ in range(5)])
                return row_data
            else:
                ticker = command[1]
                self.TICKER = ticker.upper()
                row_data = [
                    (" " * (margin)),
                    f"LOADED <{self.TICKER}>".center(margin),
                    (" " * (margin)),
                    f"${yf.Ticker(self.TICKER).history(period='1d').iloc[-1].Close:.4f}".center(margin),
                    (" " * (margin)),
                    f" DES - Company description".ljust(margin),
                    f" STAT - Company statistics and info".ljust(margin),
                    f" CN - Company news".ljust(margin),
                    f" GP - Historical price chart".ljust(margin),
                    f" GIP - Intraday price chart".ljust(margin),
                    f" DVD - Dividend information".ljust(margin),
                    f" ERN - Earnings information and summary".ljust(margin),
                    f" FA - Financial Statements".ljust(margin)
                ]
                return row_data
        except Exception as e:
            row_data = []
            row_data.append(f'{f'<{type(e).__name__}> Exception':^{margin}}')
            row_data.append(f'{f'<{command[1].upper()}> is not a valid symbol.':^{margin}}')
            row_data.append((" " * (margin)))
            return row_data
    
    def equity_command_des(self, TERMINAL_WIDTH: int) -> list:
        margin = TERMINAL_WIDTH - 4
        color = 5
        reset = 4
        info = yf.Ticker(self.TICKER).info
        row_data = [
                    (" " * (margin)),
                    f"LOADED <{self.TICKER}>".center(margin),
                    (" " * (margin)),
                    f"{Fore.CYAN}{info["longName"]}{Style.RESET_ALL}".ljust(margin + color + reset),
                    f"Industry {info["industry"]}".rjust(margin),                    
                ]
        # Fix long summary overflow
        long_summary = info["longBusinessSummary"]
        while len(long_summary) > margin:
            space_index = long_summary.rfind(" ", 0, margin)
            if space_index == -1:
                row_data.append(f"{long_summary[:margin]}".ljust(margin))
                long_summary = long_summary[margin:]
            else:
                row_data.append(f"{long_summary[:space_index]}".ljust(margin))
                long_summary = long_summary[space_index + 1:]

        # Add last part of long_summary
        row_data.append(f"{long_summary}".ljust(margin),)
        row_data.append((" " * (margin)))
        row_data.append(f"Corporate Info".ljust(margin))
        row_data.append(f"{info["website"]}".ljust(margin))
        row_data.append(f"{info["phone"]}".ljust(margin))
        
        row_data.append(f"{f"{info["country"]}, {info["state"]}, {info["city"]}, {info["address1"]}"}".ljust(margin))
        
        
        return row_data
    
    def equity_command_stat(self, TERMINAL_WIDTH: int) -> list:
        row_data = []
        return row_data
    
    def equity_command_cn(self, TERMINAL_WIDTH: int) -> list:
        row_data = []
        return row_data
    
    def equity_command_gp(self, TERMINAL_WIDTH: int) -> list:
        row_data = []
        return row_data
    
    def equity_command_gip(self, TERMINAL_WIDTH: int) -> list:
        row_data = []
        return row_data
    
    def equity_command_dvd(self, TERMINAL_WIDTH: int) -> list:
        row_data = []
        return row_data
    
    def equity_command_ern(self, TERMINAL_WIDTH: int) -> list:
        row_data = []
        return row_data
    
    def equity_command_fa(self, TERMINAL_WIDTH: int) -> list:
        row_data = []
        return row_data