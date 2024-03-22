import unittest
import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.data.fetch_data import fetch_stock_data
from src.data.process_data import prepare_data
from src.data.save_data import save_data_to_csv, save_data_to_db, StockData

class TestDataIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Setup for the entire test case (run once before all tests)
        cls.ticker_symbol = "AAPL"
        cls.start_date = "2020-01-01"
        cls.end_date = "2020-01-31"
        cls.csv_filename = 'test_stock_data.csv'
        cls.database_url = 'sqlite:///test_stock_data.db'
        # Ensure the database and CSV file do not exist before starting the tests
        if os.path.exists(cls.csv_filename):
            os.remove(cls.csv_filename)
        if os.path.exists(cls.database_url.split('///')[-1]):
            os.remove(cls.database_url.split('///')[-1])

    def test_data_pipeline(self):
        # Fetch stock data
        data = fetch_stock_data(self.ticker_symbol, self.start_date, self.end_date)
        self.assertIsNotNone(data)
        self.assertFalse(data.empty)

        # Process data
        train_data, _ = prepare_data(data)
        self.assertFalse(train_data.empty)
        # Do a quick check for rsi and ma_5 columns
        self.assertIn('ma_5', train_data.columns)
        self.assertIn('rsi', train_data.columns)

        # Save data to CSV
        save_data_to_csv(train_data, self.csv_filename)
        self.assertTrue(os.path.exists(self.csv_filename))

        # Save data to DB
        save_data_to_db(train_data, self.database_url)
        # Verify data is saved in DB
        engine = create_engine(self.database_url)
        Base = declarative_base()
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        result = session.query(StockData).all()
        self.assertGreater(len(result), 0)
        session.close()

    @classmethod
    def tearDownClass(cls):
        # Clean up after the entire test case (run once after all tests)
        if os.path.exists(cls.csv_filename):
            os.remove(cls.csv_filename)
        if os.path.exists(cls.database_url.split('///')[-1]):
            os.remove(cls.database_url.split('///')[-1])

if __name__ == '__main__':
    unittest.main()
