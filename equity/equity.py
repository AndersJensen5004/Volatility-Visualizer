import yfinance as yf

class Equity:
    @classmethod
    def equity_command(cls, command: list, TERMINAL_WIDTH: int) -> list:
        """Loads a symbol main menu for commands

        Args:
            command (list): list of command arguments
            TERMINAL_WIDTH (int): width of terminal window

        Returns:
            list: row_data of command list for equity
        """
        
        margin = TERMINAL_WIDTH - 4
        
        row_data = [f"{'Invalid Arguments -> Use equity <symbol>':^{margin}}"] if len(command) != 2 else [
            (" " * (margin)),
            f"LOADED <{command[1].upper()}>".center(margin),
            (" " * (margin)),
            f"${yf.Ticker(command[1]).history(period='1d').iloc[-1].Close:.4f}".center(margin),
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

    #    except Exception as e:
    #        row_data.append(f'{f'<{type(e).__name__}> Exception':^{margin}}')
    #        row_data.append(f'{f'<{command[1].upper()}> is not a valid symbol.':^{margin}}')
    #        row_data.append((" " * (margin)))
    #        return row_data