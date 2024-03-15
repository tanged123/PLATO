import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def clean_data(data):
    """
    Cleans data from the DataFrame.

    Parameters:
    - data (pandas.DataFrame): The input DataFrame containing stock data.

    Returns:
    - pandas.DataFrame: A DataFrame with rows containing NaN values removed.
    """

    # TODO, figure out what else needs to be cleaned up\
    # Removes missing rows
    cleaned_data = data.dropna() 
    # Remove duplicates, keeping the first occurrence
    cleaned_data = cleaned_data.drop_duplicates(subset='date', keep='first')

    return cleaned_data

def add_moving_average(data, window_size=5):
    """
    Calculate and add a new column to the DataFrame for the moving average of the 'close' prices over a specified window size.

    Parameters:
    - data (pandas.DataFrame): The input DataFrame containing stock data.
    - window_size (int): The number of periods to use for calculating the moving average.

    Returns:
    - pandas.DataFrame: The input DataFrame with an additional column ('MA_{window_size}') representing the moving average.
    """

    # TODO, may be adding NaNs here
    data[f'MA_{window_size}'] = data['close'].rolling(window=window_size).mean()
    return data

def add_rsi(data, window_size=14):
    """
    Calculate and add a new column to the DataFrame for the Relative Strength Index (RSI) of the 'close' prices over a specified window size.

    Parameters:
    - data (pandas.DataFrame): The input DataFrame containing stock data.
    - window_size (int): The number of periods to use for calculating the RSI.

    Returns:
    - pandas.DataFrame: The input DataFrame with an additional column ('RSI') representing the Relative Strength Index.
    """

    # TODO, may be adding NaNs here
    delta = data['close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=window_size).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window_size).mean()
    RS = gain / loss
    data['RSI'] = 100 - (100 / (1 + RS))
    return data

def normalize_features(data):
    """
    Standardize features in the DataFrame by removing the mean and scaling to unit variance. This is commonly done before training machine learning models.

    Parameters:
    - data (pandas.DataFrame): The input DataFrame containing stock data.

    Returns:
    - pandas.DataFrame: The DataFrame with specified features standardized.
    """

    #TODO normalize features may not be correct, test case needed lots of leeway, 24% off normalization
    #     Also may be having some runtime warnings of almost invalid values
    scaler = StandardScaler()
    features = ['open', 'high', 'low', 'close', 'volume', 'MA_5', 'RSI']

    #fit_transform our data features        
    data[features] = scaler.fit_transform(data[features])
    return data

def pad_missing_values(data,ma_window_size):
    """
    Meant to pad out the beginning and end of MA5 and RSI values

    Parameters:
    - data (pandas.DataFrame): The input DataFrame containing stock data.

    Returns:
    - pandas.DataFrame: The DataFrame with MA5 and RSI padded
    """
    data[f'MA_{ma_window_size}'] = data[f'MA_{ma_window_size}'].fillna(method='ffill').fillna(method='bfill')
    data['RSI'] = data['RSI'].fillna(method='ffill').fillna(method='bfill')
    return data

def prepare_data(data, test_size=0.2, ma_window_size=5, rsi_window_size=14):
    """
    Prepares the data for modeling, including sorting by date and performing a train-test split.

    Parameters:
    - data (pandas.DataFrame): The input DataFrame containing the stock data.
    - test_size (float): The proportion of the dataset to include in the test split.
    - random_state (int, optional): Controls the shuffling applied to the data before applying the split.

    Returns:
    - tuple: A tuple containing the training and testing datasets.
    """
    # Run through preprocessing before splitting
    data = clean_data(data)
    data = add_moving_average(data,ma_window_size)
    data = add_rsi(data,rsi_window_size)
    data = normalize_features(data)
    data = pad_missing_values(data,ma_window_size)
    #data = clean_data(data) # clean data again to remove any nans added by adding features
    
    data.sort_values(by='date', inplace=True)  # Sort the DataFrame by 'date', assumes no duplicates

    # After sorting, there's no need to assign to another variable for the length calculation
    split_idx = int(len(data) * (1 - test_size))  # Use the sorted DataFrame directly

    # Perform the train-test split based on the calculated index
    train = data.iloc[:split_idx]
    test = data.iloc[split_idx:]

    return train, test

# Example usage
if __name__ == "__main__":
    # Assume `data` is your DataFrame loaded from CSV
    data = pd.read_csv('your_stock_data.csv')
    train_data, test_data = prepare_data(data)
    print(train_data.head(), test_data.head())
