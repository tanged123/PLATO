# tests/test_features.py

import unittest
import pandas as pd
from src.features.build_features import add_moving_averages, add_rsi, add_bollinger_bands, build_features

class TestFeatureEngineering(unittest.TestCase):

    def setUp(self):
        """Set up test data for the feature engineering functions."""
        self.data = pd.DataFrame({
            'close': list(range(10, 110, 2))  # Creates a sequence from 10 to 110, incrementing by 2
        })

    def test_add_moving_averages(self):
        """Test the add_moving_averages function."""
        result = add_moving_averages(self.data.copy(), windows=[2, 4])
        self.assertIn('ma_2', result.columns)
        self.assertIn('ma_4', result.columns)
        # Test for a specific value to ensure calculations are correct
        # Asserts second to last moving average
        self.assertAlmostEqual(result['ma_2'].iloc[-1], 107, places=1)
        self.assertAlmostEqual(result['ma_4'].iloc[-1], 105, places=1)

    def test_add_rsi(self):
        """Test the add_rsi function."""
        result = add_rsi(self.data.copy())
        self.assertIn('rsi', result.columns)
        # Simply verify the presence and non-NaN nature
        # of the 'rsi' column for now.
        # TODO: me being lazy, implement actual calculated value comparison later
        self.assertFalse(result['rsi'].isnull().all())

    def test_add_bollinger_bands(self):
        """Test the add_bollinger_bands function."""
        result = add_bollinger_bands(self.data.copy())
        self.assertIn('bb_high', result.columns)
        self.assertIn('bb_low', result.columns)
        # Similar to RSI, verify the bands are calculated at all
        # TODO: me being lazy, implement actual calculated value comparison later
        self.assertFalse(result['bb_high'].isnull().all())
        self.assertFalse(result['bb_low'].isnull().all())

if __name__ == '__main__':
    unittest.main()