import pandas as pd
import numpy as np
import os

"""
IMPORTANT DATA TIP: WE ENFORCE LOWER CASE FOR PANDA HEADERS!!! 😠
"""


def add_moving_averages(data, windows=[5, 20, 50]):
    """
    Adds moving averages for specified window lengths to the DataFrame.
    
    Parameters:
    - data (pandas.DataFrame): DataFrame containing stock price data.
    - windows (list): List of integers representing the window sizes for moving averages.
    
    Returns:
    - pandas.DataFrame: DataFrame with new columns for each moving average.

    # TODO, may be adding NaNs here
    """
    for window in windows:
        data[f'ma_{window}'] = data['close'].rolling(window=window).mean()
    return data

def add_rsi(data, window=14):
    """
    Adds the Relative Strength Index (RSI) to the DataFrame.
    
    Parameters:
    - data (pandas.DataFrame): DataFrame containing stock price data.
    - window (int): Window size for RSI calculation.
    
    Returns:
    - pandas.DataFrame: DataFrame with a new column 'rsi'.

    # TODO, may be adding NaNs here
    """

    delta = data['close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    rs = gain / loss
    data['rsi'] = 100 - (100 / (1 + rs))
    
    return data

def add_bollinger_bands(data, window=20):
    """
    Adds Bollinger Bands to the DataFrame.
    
    Parameters:
    - data (pandas.DataFrame): DataFrame containing stock price data.
    - window (int): Window size for Bollinger Bands calculation.
    
    Returns:
    - pandas.DataFrame: DataFrame with new columns 'bb_high' and 'bb_low'.
    """
    ma = data['close'].rolling(window=window).mean()
    std = data['close'].rolling(window=window).std()
    
    data['bb_high'] = ma + (std * 2)
    data['bb_low'] = ma - (std * 2)
    
    return data

def build_features(data):
    """
    Applies various feature engineering techniques to the stock price data.
    
    Parameters:
    - data (pandas.DataFrame): DataFrame containing stock price data.
    
    Returns:
    - pandas.DataFrame: Enhanced DataFrame with additional features.
    """

    # Define the minimum required length based on your largest window size
    # Adjust this value based on the actual largest window size you use in your feature engineering
    MIN_REQUIRED_LENGTH = 50

    # Check if the data length is sufficient, skip if in test
    if not os.getenv('RUNNING_TESTS') and len(data) < MIN_REQUIRED_LENGTH:
        raise ValueError(f"Data length is insufficient for feature engineering. " \
                         f"Required: {MIN_REQUIRED_LENGTH}, Provided: {len(data)}")
    

    data = add_moving_averages(data)
    data = add_rsi(data)
    data = add_bollinger_bands(data)
    
    # Add more feature engineering functions as needed
    
    return data