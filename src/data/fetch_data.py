# src/data/fetch_data.py

import yfinance as yf
import pandas as pd
import uuid

def fetch_stock_data(ticker_symbol, start_date, end_date):
    """
    Fetches historical stock data for a given ticker symbol from Yahoo Finance,
    and includes the ticker symbol and a unique ID for each row.

    Parameters:
    - ticker_symbol (str): The ticker symbol of the stock (e.g., 'AAPL').
    - start_date (str): The start date for the data fetch (format: 'YYYY-MM-DD').
    - end_date (str): The end date for the data fetch (format: 'YYYY-MM-DD').

    Returns:
    - pandas.DataFrame: DataFrame containing the fetched stock data along with an 'id' and 'symbol' column.
    """
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(start=start_date, end=end_date)
    data.reset_index(inplace=True) # Reset index and get date as just another data field
    # Include the ticker symbol as a column
    data['symbol'] = ticker_symbol.upper()  # Assuming you want the symbol in uppercase
    # Inside your fetch_stock_data function, after resetting the index
    data['id'] = [str(uuid.uuid4()) for _ in range(len(data))]
    # Convert column names to lowercase
    data.columns = data.columns.str.lower()
    data['date'] = pd.to_datetime(data['date']).dt.date # Convert datetime value
    return data

if __name__ == "__main__":
    # Example usage
    symbol = "AAPL"
    start = "2020-01-01"
    end = "2021-01-01"
    data = fetch_stock_data(symbol, start, end)
    print(data.head())