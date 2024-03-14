import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def clean_data(data):
    # TODO, figure out what else needs to be cleaned up
    cleaned_data = data.dropna()
    return cleaned_data

def add_moving_average(data, window_size=5):
    # TODO, may be adding NaNs here
    data[f'MA_{window_size}'] = data['close'].rolling(window=window_size).mean()
    return data

def add_rsi(data, window_size=14):
    # TODO, may be adding NaNs here
    delta = data['close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=window_size).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window_size).mean()
    RS = gain / loss
    data['RSI'] = 100 - (100 / (1 + RS))
    return data

def normalize_features(data):
    #TODO normalize features may not be correct, test case needed lots of leeway, 24% off normalization
    #     Also may be having some runtime warnings of almost invalid values
    scaler = StandardScaler()
    features = ['open', 'high', 'low', 'close', 'volume', 'MA_5', 'RSI']

    #fit_transform our data features        
    data[features] = scaler.fit_transform(data[features])
    return data

def prepare_data(data):
    data = clean_data(data)
    data = add_moving_average(data)
    data = add_rsi(data)
    data = normalize_features(data)
    # Splitting data into train, validate, test
    train, test = train_test_split(data, test_size=0.2, random_state=42)
    return train, test

# Example usage
if __name__ == "__main__":
    # Assume `data` is your DataFrame loaded from CSV
    data = pd.read_csv('your_stock_data.csv')
    train_data, test_data = prepare_data(data)
    print(train_data.head(), test_data.head())
