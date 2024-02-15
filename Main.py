# Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta


def main():
    year = datetime.now().year
    month = datetime.now().month
    third_friday = third_friday_of_month(year, month)
    print(third_friday)
        
    print("test")



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


    
# Run
if __name__ == "__main__":
    main()