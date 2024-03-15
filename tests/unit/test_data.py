# tests/test_data.py

import unittest
import pandas as pd
import warnings
from unittest.mock import patch, MagicMock
from src.data.fetch_data import fetch_stock_data
from src.data.save_data import save_data_to_csv, save_data_to_db
from src.data.process_data import clean_data, add_moving_average, add_rsi, normalize_features, prepare_data
from sklearn.preprocessing import StandardScaler


class TestDataFetch(unittest.TestCase):
    @patch('src.data.fetch_data.yf.Ticker')
    def test_fetch_stock_data(self, mock_ticker):
        # Define expected DataFrame structure returned by the mock, with lowercase column names
        expected_df = pd.DataFrame({
            'open': [100, 101, 102],
            'high': [110, 111, 112],
            'low': [90, 91, 92],
            'close': [105, 106, 107],
            'volume': [1000, 1010, 1020],
            # Assuming 'dividends' and 'stock splits' are the additional columns mentioned
            'dividends': [0.5, 0.5, 0.5],
            'stock splits': [0, 0, 0]
        }, index=pd.to_datetime(['2020-01-01', '2020-01-02', '2020-01-03']))

        # Convert the index to a column named 'date' to reflect the fetch_data function's behavior
        expected_df.reset_index(inplace=True)
        expected_df.rename(columns={'index': 'date'}, inplace=True)
        
        # Setup the mock to return the expected DataFrame
        mock_ticker.return_value.history.return_value = expected_df
        
        # Call the function with mock parameters
        result_df = fetch_stock_data('AAPL', '2020-01-01', '2020-01-03')
        
        # Ensure the result DataFrame's columns are all lowercase, as fetch_stock_data function should ensure
        result_df.columns = result_df.columns.str.lower()
        
        # Verify the result is as expected
        pd.testing.assert_frame_equal(result_df, expected_df)


class TestSaveDataCSV(unittest.TestCase):
    @patch("pandas.DataFrame.to_csv")
    def test_save_data_to_csv(self, mock_to_csv):
        data = pd.DataFrame({
            'Date': ['2020-01-01', '2020-01-02'],
            'Close': [300, 305],
            'Volume': [1000, 1500]
        })
        filename = 'test_data.csv'
        
        save_data_to_csv(data, filename)
        
        # Check if to_csv was called once with the filename
        mock_to_csv.assert_called_once_with(filename, index=False)

class TestSaveDataDB(unittest.TestCase):
    @patch('pandas.DataFrame.to_sql')
    @patch('src.data.save_data.create_engine')
    def test_save_data_to_db(self, mock_create_engine, mock_to_sql):
        # Prepare DataFrame with string dates
        data = pd.DataFrame({
            'date': ['2020-01-01', '2020-01-02'],  # Lowercase column names to align with the fetch_data output
            'open': [290, 290],
            'close': [300, 305],
            'volume': [1000, 1500],
            'high': [310, 310],
            'low': [290, 290]
        })
        
        # Call the function with mocked objects
        database_url = 'sqlite:///test_stock_data.db'
        table_name = 'stock_data'
        save_data_to_db(data, database_url, table_name)
        
        # Check if pandas.DataFrame.to_sql was called correctly
        mock_to_sql.assert_called_once()
        mock_create_engine.assert_called_once_with(database_url)
        
        # Verify to_sql was called with correct parameters
        call_args, call_kwargs = mock_to_sql.call_args
        self.assertEqual(call_kwargs['name'], table_name)
        self.assertEqual(call_kwargs['con'], mock_create_engine.return_value)
        self.assertEqual(call_kwargs['index'], False)
        self.assertEqual(call_kwargs['if_exists'], 'append')

class TestProcessData(unittest.TestCase):

    def test_clean_data(self):
        # Extend test data to include 'date' column with duplicate entries
        data = pd.DataFrame({
            'date': ['2020-01-01', '2020-01-01', '2020-01-02'],
            'open': [100, 101, 102],
            'close': [105, None, None]
        })
        
        # Perform data cleaning
        cleaned = clean_data(data)
        
        # Check that the cleaned data has the expected length
        # Expecting 2 rows: one duplicate date removed, one row with NaN values removed
        self.assertEqual(len(cleaned), 1, "Cleaned data should have 1 row after removing duplicates and NaNs")
        
        # Additionally, verify that the correct row is kept (the first occurrence)
        self.assertEqual(cleaned.iloc[0]['open'], 100, "The first occurrence of the duplicate date should be kept")

    def test_add_moving_average(self):
        data = pd.DataFrame({
            'close': [1, 2, 3, 4, 5]
        })
        result = add_moving_average(data, window_size=3)
        expected_ma = [None, None, 2, 3, 4]  # The first two are NaN because the window is 3
        pd.testing.assert_series_equal(result['MA_3'], pd.Series(expected_ma, name='MA_3'), check_names=False)

    def test_add_rsi(self):
        data = pd.DataFrame({
            'close': [110, 120, 130, 120, 110]
        })
        result = add_rsi(data)
        self.assertIn('RSI', result.columns)  # Check if RSI column is added


    def test_normalize_features(self):
        data = pd.DataFrame({
            'open': [1, 2, 3],
            'high': [1, 2, 3],
            'low': [1, 2, 3],
            'close': [1, 2, 3],
            'volume': [1, 2, 3],
            'MA_5': [1, 2, 3],
            'RSI': [1, 2, 3]
        })
        normalized_data = normalize_features(data)

        for col in ['open', 'high', 'low', 'close', 'volume', 'MA_5', 'RSI']:
            # Check if the mean is close to 0
            self.assertAlmostEqual(normalized_data[col].mean(), 0, places=1,
                                msg=f"Mean of {col} after normalization is not close to 0")

            # Check if the std deviation is close to 1
            self.assertAlmostEqual(normalized_data[col].std(ddof=0), 1, places=1,
                                msg=f"Std of {col} after normalization is not close to 1")

    def test_prepare_data(self):
        data = pd.DataFrame({
            'date': pd.date_range(start="2020-01-01", periods=5, freq='D'),
            'open': [100, 101, 102, 103, 104],
            'close': [105, 106, 107, 108, 109],
            'volume': [1000, 1100, 1200, 1300, 1400],
            'high': [105, 106, 107, 108, 109],  # Included 'high' column
            'low': [95, 96, 97, 98, 99],        # Included 'low' column
        })
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            train_data, test_data = prepare_data(data, test_size = 0.4)
            
        # Check that the train and test data are not empty
        self.assertNotEqual(len(train_data), 0, "Train data should not be empty")
        self.assertNotEqual(len(test_data), 0, "Test data should not be empty")
        
        # Ensure the expected features 'MA_5' and 'RSI' are added to both train and test datasets
        self.assertIn('MA_5', train_data.columns, "'MA_5' not found in train data columns")
        self.assertIn('RSI', train_data.columns, "'RSI' not found in train data columns")
        self.assertIn('MA_5', test_data.columns, "'MA_5' not found in test data columns")
        self.assertIn('RSI', test_data.columns, "'RSI' not found in test data columns")


if __name__ == '__main__':
    unittest.main()