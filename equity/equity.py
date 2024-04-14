import curses
import yfinance as yf

equity_commands = [
    " LOAD - Loads equity",
    " DES - Company description",
    " STAT - Company statistics and info",
    " CN - Company news",
    " GP - Historical price chart",
    " GIP - Intraday price chart",
    " DVD - Dividend information",
    " ERN - Earnings information and summary",
    " FA - Financial Statements"
]


class Equity:

    def __init__(self, ticker):
        self.TICKER = ticker

    def execute_command(self, p, command: list) -> None:
        command_mappings = {
            "load": lambda: (self.equity_command_load(p, command)),
            "des": lambda: (self.equity_command_des(p, command)),
            "stat": lambda: (self.equity_command_stat(p, command)),
            "cn": lambda: (self.equity_command_cn(p, command)),
            "gp": lambda: (self.equity_command_gp(p, command)),
            "gip": lambda: (self.equity_command_gip(p, command)),
            "dvd": lambda: (self.equity_command_dvd(p, command)),
            "ern": lambda: (self.equity_command_ern(p, command)),
            "fa": lambda: (self.equity_command_fa(p, command)),
            "_default": lambda: (self.equity_invalid_command(p, command)),
        }
        # Second Argument
        try:
            command_function = command_mappings.get(command[1], command_mappings["_default"])
        except IndexError:
            if self.TICKER is None:
                command_function = command_mappings["_default"]
            else:
                command_function = lambda: (self.equity_command_load(p, ["equity", "load", self.TICKER]))
        # Execute
        command_function()

    @staticmethod
    def equity_invalid_command(p, command: list) -> None:

        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_BLACK)

        arguments = ' '.join(f'<{arg}>' for arg in command)
        invalid_usage = f"Invalid Command Usage >>> {arguments}"
        invalid_y, invalid_x = p.getmaxyx()
        # **CHANGED invalid_y TO 9 TESTING PAD**
        invalid_y = 9
        # Center horizontally, ensuring invalid_x is non-negative
        invalid_x = max((invalid_x - len(invalid_usage)) // 2, 0)
        p.addstr(invalid_y // 3, invalid_x, invalid_usage, curses.color_pair(4))

        correct_usage = [
            "Use <equity> <load> <TICKER>",
            "OR <equity> <load> <TICKER> <menu>",
            "OR <equity> <menu>"
        ]
        correct_y = (invalid_y // 3) + 2  # Place correct usage below invalid usage
        correct_x = (invalid_x + 4)  # Indent correct usage slightly
        for usage in correct_usage:
            p.addstr(correct_y, correct_x, usage, curses.color_pair(3))
            correct_y += 1

        description_y = correct_y + 2  # Place descriptions below correct usage
        description_x = 1  # Left-align descriptions
        for c in equity_commands:
            p.addstr(description_y, description_x, c, curses.color_pair(10))
            description_y += 1

    def equity_command_load(self, p, command: list) -> None:
        """Loads a symbol main menu for commands

        Args:
            p (curses pad): curses pad
            command (list): list of command arguments

        """

        curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

        try:
            ticker = command[2]
        except IndexError:
            self.equity_invalid_command(p, command)
            return

        self.TICKER = ticker.upper()
        price = yf.Ticker(self.TICKER).history(period='1d').iloc[-1].Close
        if price > 1:
            price_string = f"${price:.2f}"
        else:
            price_string = f"${price:.4f}"

        data = [
            f"LOADED <{self.TICKER}>",
            price_string,
        ]

        # Print data centered and in orange
        data_y, data_x = p.getmaxyx()
        data_x = (data_x - max(len(line) for line in data)) // 2  # Center horizontally
        center_y = data_y // 6
        for line in data:
            p.addstr(center_y, data_x, line, curses.color_pair(6))
            center_y += 1

        # Print descriptions in white
        description_y = center_y + 2  # Place descriptions below data
        description_x = 1  # Left-align descriptions
        for c in equity_commands:
            p.addstr(description_y, description_x, c, curses.color_pair(10))
            description_y += 1

    def equity_command_des(self, p, command: list) -> None:
        info = yf.Ticker(self.TICKER).info
        pass

    def equity_command_stat(self, p, command: list) -> None:
        pass

    def equity_command_cn(self, p, command: list) -> None:
        pass

    def equity_command_gp(self, p, command: list) -> None:
        pass

    def equity_command_gip(self, p, command: list) -> None:
        pass

    def equity_command_dvd(self, p, command: list) -> None:
        pass

    def equity_command_ern(self, p, command: list) -> None:
        pass

    def equity_command_fa(self, p, command: list) -> None:
        pass
