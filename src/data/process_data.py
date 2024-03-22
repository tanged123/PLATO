import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
from src.features.build_features import build_features

"""
IMPORTANT DATA TIP: WE ENFORCE LOWER CASE FOR PANDA HEADERS!!! 😠
"""

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

def normalize_features(data):
    """
    Standardize all numeric features in the DataFrame by removing the mean and scaling to unit variance.
    Numeric columns are automatically detected and normalized.

    Parameters:
    - data (pandas.DataFrame): The input DataFrame containing stock data.

    Returns:
    - pandas.DataFrame: The DataFrame with numeric features standardized.
    """
    scaler = StandardScaler()
    
    # Detect numeric columns (excluding columns like 'id', 'symbol', or date columns if present)
    numeric_features = data.select_dtypes(include=[np.number]).columns.tolist()
    
    # Fit_transform only the numeric features
    data[numeric_features] = scaler.fit_transform(data[numeric_features])
    
    return data

def pad_missing_values(data):
    """
    Pads missing values for all columns in the DataFrame by applying forward fill 
    followed by backward fill. This method works for all data types.

    Parameters:
    - data (pandas.DataFrame): The input DataFrame containing stock data.

    Returns:
    - pandas.DataFrame: The DataFrame with missing values padded for all columns.
    """
    for column in data.columns:
        # Check if the column is numeric or categorical/textual
        if pd.api.types.is_numeric_dtype(data[column]):
            # For numeric columns, apply forward fill and backward fill
            data[column] = data[column].fillna(method='ffill').fillna(method='bfill')
        else:
            # For non-numeric columns, we'll also apply ffill and bfill for simplicity.
            # TODO?: potentially adjust later if non-numeric features aded
            data[column] = data[column].fillna(method='ffill').fillna(method='bfill')

    return data

def prepare_data(data, test_size=0.2):
    """
    Prepares the data for modeling, including sorting by date and performing a train-test split.
    Assumes that you have a data size that is sufficiently the MIN_REQUIRED_LENGTH

    Parameters:
    - data (pandas.DataFrame): The input DataFrame containing the stock data.
    - test_size (float): The proportion of the dataset to include in the test split.
    - random_state (int, optional): Controls the shuffling applied to the data before applying the split.

    Returns:
    - tuple: A tuple containing the training and testing datasets.
    """
    # Run through preprocessing before splitting
    data = clean_data(data) # Clean raw data
    data = build_features(data) # Add features

    if not os.getenv('RUNNING_TESTS'): #skip normalization in test
        data = normalize_features(data) # Normalize Data

    data = pad_missing_values(data) # Pad missing values
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
