# src/data/fetch_data.py

import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker_symbol, start_date, end_date):
    """
    Fetches historical stock data for a given ticker symbol from Yahoo Finance.

    Parameters:
    ticker_symbol (str): The ticker symbol of the stock (e.g., 'AAPL').
    start_date (str): The start date of the period (YYYY-MM-DD).
    end_date (str): The end date of the period (YYYY-MM-DD).

    Returns:
    pandas.DataFrame: Stock data (date, open, high, low, close, volume).
    """
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(start=start_date, end=end_date)
    return data

if __name__ == "__main__":
    # Example usage
    symbol = "AAPL"
    start = "2020-01-01"
    end = "2021-01-01"
    data = fetch_stock_data(symbol, start, end)
    print(data.head())