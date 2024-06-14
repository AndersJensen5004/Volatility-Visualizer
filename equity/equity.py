import time
import tkinter as tk
from tkinter import ttk
import yfinance as yf


class Equity:

    # Equity Commands
    equity_commands = [
        " LOAD - Loads equity",
        " DES - Company description",
        " STAT - Company statistics and info",
        " CN - Company news",
        " GP - Historical price chart",
        " GIP - Intraday price chart",
        " DVD - Dividend information",
        " ERN - Earnings information and summary",
        " FA - Financial Statements",
        " FEED - Price feed"
    ]

    @staticmethod
    def format_number(number: int) -> str:
        if number >= 1e9:
            return f"{number / 1e9:.2f}B"
        elif number >= 1e6:
            return f"{number / 1e6:.2f}M"
        elif number >= 1e3:
            return f"{number / 1e3:.2f}K"
        else:
            return f"{number:.2f}"

    @staticmethod
    def format_price(price: float) -> str:
        if price >= 1:
            return f"${price:.2f}"
        else:
            return f"${price:.4f}"

    def __init__(self, ticker):
        self.TICKER = ticker

    def execute_command(self, output, args: list) -> None:

        command_mappings = {
            "load": lambda: self.equity_command_load(output, args),
            "des": lambda: self.equity_command_des(output, args),
            "stat": lambda: self.equity_command_stat(output, args),
            "cn": lambda: self.equity_command_cn(output, args),
            "gp": lambda: self.equity_command_gp(output, args),
            "gip": lambda: self.equity_command_gip(output, args),
            "dvd": lambda: self.equity_command_dvd(output, args),
            "ern": lambda: self.equity_command_ern(output, args),
            "fa": lambda: self.equity_command_fa(output, args),
            "feed": lambda: self.equity_command_feed(output, args),
            "_default": lambda: self.equity_invalid_command(output, args),
        }
        # Second Argument
        try:
            command_function = command_mappings.get(args[1], command_mappings["_default"])
        except IndexError:
            if self.TICKER is None:
                command_function = command_mappings["_default"]
            else:
                command_function = lambda: (self.equity_command_load(output, ["equity", "load", self.TICKER]))
        # Execute
        command_function()

    @staticmethod
    def equity_invalid_command(output, args: list) -> None:
        """
        Handles an invalid command for equity and displays the correct usage in the output widget.

        Args:
            output (tkinter.Frame): The output widget to display the invalid command and correct usage.
            args (list): The list of invalid command arguments.

        Returns:
            None
        """
        output_text = tk.Text(output, height=20, width=80, font=('Poppins', 12), wrap='word', highlightthickness=0,
                              bd=0,
                              background="#b3b2af")
        output_text.pack(expand=True, fill='both', padx=8, pady=6)

        output_text.tag_configure("green_tag", foreground="#0b9925")
        output_text.tag_configure("red_tag", foreground="#a82d3c")

        arguments = ' '.join(f'<{arg}>' for arg in args)
        invalid_usage = f"Invalid Command Usage >>> {arguments}\n"

        output_text.insert(tk.END, invalid_usage, "red_tag")

        correct_usage = [
            "\nUse <equity> <load> <TICKER>",
            "OR <equity> <load> <TICKER> <menu>",
            "OR <equity> <menu>\n"
        ]
        for line in correct_usage:
            output_text.insert(tk.END, line + "\n", "green_tag")
        for line in Equity.equity_commands:
            output_text.insert(tk.END, line + "\n")
        output_text.config(state="disabled")

    def equity_command_load(self, output, args: list) -> None:
        try:
            ticker = args[2]
        except IndexError:
            self.equity_invalid_command(output, args)
            return

        output_text = tk.Text(output, height=20, width=80, font=('Poppins', 12), wrap='word', highlightthickness=0,
                              bd=0,
                              background="#b3b2af")
        output_text.pack(expand=True, fill='both', padx=8, pady=6)

        # Get ticker symbol
        self.TICKER = ticker.upper()

        # Get price
        price = yf.Ticker(self.TICKER).history(period='1d').iloc[-1].Close
        price_string = Equity.format_price(price)
        data = [
            f"LOADED <{self.TICKER}>",
            price_string,
        ]
        output_text.tag_configure("blue_tag_center", foreground="#25768a", justify="center",
                                  font=("Poppins", 12, "bold"))
        output_text.tag_configure("green_tag", foreground="#0b9925")
        for line in data:
            output_text.insert(tk.END, line + "\n", "blue_tag_center")
        for line in Equity.equity_commands:
            output_text.insert(tk.END, line + "\n", "green_tag")
        output_text.config(state="disabled")

    def equity_command_des(self, output, args: list) -> None:

        description_text = tk.Text(output, height=10, width=80, font=('Poppins', 12), wrap='word', highlightthickness=0,
                                   bd=0, background="#b3b2af")
        description_text.pack(expand=True, fill='both', padx=8, pady=6)

        info = yf.Ticker(self.TICKER).info
        name = info["longName"]
        description = info["longBusinessSummary"]
        industry = info["industry"]

        description_text.tag_configure("blue_tag_bold", foreground="#25768a", font=("Poppins", 12, "bold"))
        description_text.tag_configure("orange_tag", foreground="#b38405")
        description_text.tag_configure("orange_tag_right", foreground="#b38405", justify="right")
        description_text.tag_configure("black_tag", foreground="#242322")
        description_text.tag_configure("blue_tag", foreground="#216ccf")

        description_text.insert(tk.END, name + "\n", "blue_tag_bold")
        description_text.insert(tk.END, "Industry: ", "orange_tag_right")
        description_text.insert(tk.END, industry + "\n", "black_tag")
        description_text.insert(tk.END, description + "\n", "orange_tag")

        # Create the summary info text box
        summary_frame = ttk.Frame(output)
        summary_frame.pack(pady=5, expand=True, fill='both')

        # Price Data
        price_data_text = tk.Text(summary_frame, height=10, width=40, font=('Poppins', 12), wrap='word',
                                  highlightthickness=0, bd=0,
                                  background="#b3b2af")
        price_data_text.grid(row=0, column=0, padx=5, pady=6, sticky='nsew')
        price_data_text.tag_configure("blue_tag_bold", foreground="#25768a", font=("Poppins", 12, "bold"))
        price_data_text.tag_configure("orange_tag", foreground="#b38405", justify="left")
        price_data_text.tag_configure("orange_tag_right", foreground="#b38405", justify="right")
        price_data_text.tag_configure("black_tag_right", foreground="#242322", justify="right")
        price_data_text.tag_configure("blue_tag", foreground="#216ccf")

        # Add price data labels to price_data_frame
        currency = info["currency"]
        price_change = info["regularMarketOpen"] - info["regularMarketPreviousClose"]
        percent_change = price_change / info["regularMarketPreviousClose"] * 100
        fifty_two_week_high = info["fiftyTwoWeekHigh"]
        fifty_two_week_low = info["fiftyTwoWeekLow"]
        market_cap = info["marketCap"]
        shares_outstanding = info["sharesOutstanding"]
        float_shares = info["floatShares"]
        short_interest = info["sharesShort"]
        short_percent = info["shortPercentOfFloat"] * 100
        days_to_cover = short_interest / info["averageVolume"]
        price_data = [
            ("Price Change 1D", f"{Equity.format_price(price_change)}/{percent_change:.2f}%"),
            ("52 Week High", f"{Equity.format_price(fifty_two_week_high)}"),
            ("52 Week Low", f"{Equity.format_price(fifty_two_week_low)}"),
            ("Market Cap", Equity.format_number(market_cap)),
            ("Shares Out/Float", f"{Equity.format_number(shares_outstanding)}/{Equity.format_number(float_shares)}"),
            ("SI/% of Float", f"{Equity.format_number(short_interest)}/{short_percent:.2f}%"),
            ("Days to Cover", f"{days_to_cover:.2f}")
        ]

        for label, value in price_data:
            price_data_text.insert(tk.END, label.ljust(20), "orange_tag")
            price_data_text.insert(tk.END, value + '\n', "black_tag_right")

        # Corporate Info
        corporate_info_text = tk.Text(summary_frame, height=10, width=40, font=('Poppins', 12), wrap='word',
                                      highlightthickness=0, bd=0,
                                      background="#b3b2af")
        corporate_info_text.grid(row=0, column=1, padx=5, pady=6, sticky='nsew')
        corporate_info_text.tag_configure("blue_tag_bold", foreground="#25768a", font=("Poppins", 12, "bold"))
        corporate_info_text.tag_configure("orange_tag", foreground="#b38405")
        corporate_info_text.tag_configure("orange_tag_right", foreground="#b38405", justify="right")
        corporate_info_text.tag_configure("black_tag", foreground="#242322")
        corporate_info_text.tag_configure("blue_tag", foreground="#216ccf")

        # Add corporate info labels to corporate_info_frame
        website = info["website"]
        location = ""
        try:
            location += info["city"] + ", "
            location += info["state"] + ", "
        except KeyError:
            pass
        try:
            location += info["country"]
        except KeyError:
            pass
        employees = info["fullTimeEmployees"]

        corporate_info_text.insert(tk.END, website + "\n", "blue_tag")
        corporate_info_text.insert(tk.END, location + "\n", "orange_tag")
        corporate_info_text.insert(tk.END, "Employees ", "orange_tag")
        corporate_info_text.insert(tk.END, employees, "black_tag")

        # Other Data
        estimates_data_text = tk.Text(summary_frame, height=15, width=40, font=('Poppins', 12), wrap='word',
                                      highlightthickness=0, bd=0,
                                      background="#b3b2af")
        estimates_data_text.grid(row=0, column=2, padx=5, pady=6, sticky='nsew')
        estimates_data_text.tag_configure("orange_tag", foreground="#b38405", justify="left")
        target_high_price = info["targetHighPrice"]
        target_low_price = info["targetLowPrice"]
        target_mean_price = info["targetMeanPrice"]
        target_median_price = info["targetMedianPrice"]
        recommendation_key = info["recommendationKey"]
        number_of_estimates = info["numberOfAnalystOpinions"]
        estimate_data = [
            ("Target High", f"{Equity.format_price(target_high_price)}"),
            ("Target Low", f"{Equity.format_price(target_low_price)}"),
            ("Target Mean", f"{Equity.format_price(target_mean_price)}"),
            ("Target Median", f"{Equity.format_price(target_median_price)}"),
            ("Recommendation", f"{recommendation_key}"),
            ("Number of Estimates", f"{number_of_estimates}")
        ]
        for label, value in estimate_data:
            estimates_data_text.insert(tk.END, label.ljust(30), "orange_tag")
            estimates_data_text.insert(tk.END, value + '\n', "black_tag_right")

    def equity_command_stat(self, output, command: list) -> None:
        pass

    def equity_command_cn(self, output, command: list) -> None:
        pass

    def equity_command_gp(self, output, command: list) -> None:
        pass

    def equity_command_gip(self, output, command: list) -> None:
        pass

    def equity_command_dvd(self, output, command: list) -> None:
        pass

    def equity_command_ern(self, output, command: list) -> None:
        pass

    def equity_command_fa(self, output, command: list) -> None:
        pass

    def equity_command_feed(self, output, command: list) -> None:
        description_text = tk.Text(output, height=10, width=80, font=('Poppins', 12), wrap='word', highlightthickness=0,
                                   bd=0, background="#b3b2af")
        description_text.pack(expand=True, fill='both', padx=8, pady=6)
        description_text.tag_configure("orange_tag", foreground="#b38405")
        ticker = yf.Ticker(self.TICKER)
        while True:
            data = ticker.history(period="1d")["Close"].iloc[-1]
            description_text.insert(tk.END, f"{data}\n", "orange_tag")
            time.sleep(1)