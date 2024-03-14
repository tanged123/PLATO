import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def clean_data(data):
    """
    Remove rows with any missing values from the DataFrame.

    Parameters:
    - data (pandas.DataFrame): The input DataFrame containing stock data.

    Returns:
    - pandas.DataFrame: A DataFrame with rows containing NaN values removed.
    """

    # TODO, figure out what else needs to be cleaned up
    cleaned_data = data.dropna()
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

def prepare_data(data):
    """
    Prepare the stock data for machine learning models. This includes cleaning the data, adding moving average and RSI features, normalizing the features, and finally splitting the data into training and testing sets.

    Parameters:
    - data (pandas.DataFrame): The input DataFrame containing stock data.

    Returns:
    - tuple: A tuple containing two DataFrames, one for training and another for testing.
    """

    data = clean_data(data)
    data = add_moving_average(data)
    data = add_rsi(data)
    data = normalize_features(data)
    # Splitting data into train, validate, test
    train, test = train_test_split(data, test_size=0.3, random_state=42)
    return train, test

# Example usage
if __name__ == "__main__":
    # Assume `data` is your DataFrame loaded from CSV
    data = pd.read_csv('your_stock_data.csv')
    train_data, test_data = prepare_data(data)
    print(train_data.head(), test_data.head())
