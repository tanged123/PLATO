# tests/integration/test_features.py

import unittest
import pandas as pd
from src.features.build_features import add_moving_averages, add_rsi, add_bollinger_bands, build_features

class TestFeatureIntegration(unittest.TestCase):

    def setUp(self):
        """Set up test data for the feature engineering functions."""
        self.data = pd.DataFrame({
            'close': [10, 12, 14, 16, 18, 20, 22, 24, 26, 28]
        })

    def test_build_features(self):
        """Integration test for the build_features function."""
        result = build_features(self.data.copy())
        # Verify that all expected columns are present in the result
        expected_columns = ['close', 'ma_5', 'ma_20', 'ma_50', 'rsi', 'bb_high', 'bb_low']
        for column in expected_columns:
            self.assertIn(column, result.columns)
        # TODO: further verify the correctness of calculations for each feature

if __name__ == '__main__':
    unittest.main()