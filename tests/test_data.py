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
        # Define expected DataFrame structure returned by the mock
        expected_df = pd.DataFrame({
            'Open': [100, 101, 102],
            'High': [110, 111, 112],
            'Low': [90, 91, 92],
            'Close': [105, 106, 107],
            'Volume': [1000, 1010, 1020]
        }, index=pd.to_datetime(['2020-01-01', '2020-01-02', '2020-01-03']))
        
        # Setup the mock to return the expected DataFrame
        mock_ticker.return_value.history.return_value = expected_df
        
        # Call the function with mock parameters
        result_df = fetch_stock_data('AAPL', '2020-01-01', '2020-01-03')
        
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
    @patch('src.data.save_data.sessionmaker')
    @patch('src.data.save_data.create_engine')
    def test_save_data_to_db(self, mock_create_engine, mock_sessionmaker):
        # Setup mock session
        mock_session = MagicMock()
        mock_sessionmaker.return_value = MagicMock(return_value=mock_session)
        
        # Prepare DataFrame with string dates
        data = pd.DataFrame({
            'Date': ['2020-01-01', '2020-01-02'],
            'Open': [290, 290],
            'Close': [300, 305],
            'Volume': [1000, 1500],
            'High': [310, 310],
            'Low': [290, 290]
        })
        
        # Call the function with mocked objects
        database_url = 'sqlite:///test_stock_data.db'
        save_data_to_db(data, database_url)
        
        # Check if session methods are called appropriately
        mock_session.add.assert_called()
        mock_session.commit.assert_called()

        # Reset mock to clear call history
        mock_session.reset_mock()

class TestProcessData(unittest.TestCase):

    def test_clean_data(self):
        data = pd.DataFrame({
            'open': [100, None, 102],
            'close': [105, 107, None]
        })
        cleaned = clean_data(data)
        self.assertEqual(len(cleaned), 1)  # Expect only 1 row that has no NaN values

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
            'open': [100, 101, 102, 103, 104],
            'close': [105, 106, 107, 108, 109],
            'volume': [1000, 1100, 1200, 1300, 1400],
            'high': [105, 106, 107, 108, 109],  # Included 'high' column
            'low': [95, 96, 97, 98, 99],        # Included 'low' column
        })
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            train_data, test_data = prepare_data(data)
            
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