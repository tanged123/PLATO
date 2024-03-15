import pandas as pd
import datetime
from sqlalchemy import create_engine
from src.data.fetch_data import fetch_stock_data
from src.data.process_data import prepare_data
from src.data.save_data import save_data_to_csv, save_data_to_db

# Configuration
TICKER_SYMBOL = "^GSPC"
START_DATE = "2000-01-01"
END_DATE = datetime.datetime.now().strftime('%Y-%m-%d')
CSV_FILENAME = "S&P_stock_data.csv"
DATABASE_URL = "sqlite:///S&P_stock_data.db"
TABLE_NAME = "stock_data"

def run_data_pipeline(ticker_symbol, start_date, end_date, csv_filename, database_url, table_name):
    # Fetch stock data
    print(f"Fetching data for {ticker_symbol} from {start_date} to {end_date}...")
    data = fetch_stock_data(ticker_symbol, start_date, end_date)
    
    # Process the data
    print("Processing data...")
    train_data, _ = prepare_data(data,0.1)
    
    # Save the processed data to a CSV file
    print(f"Saving data to {csv_filename}...")
    save_data_to_csv(train_data, csv_filename)
    
    # Save the processed data to a database
    print(f"Saving data to database {database_url}, table {table_name}...")
    save_data_to_db(train_data, database_url, table_name)
    
    print("Data pipeline completed successfully.")

if __name__ == "__main__":
    run_data_pipeline(TICKER_SYMBOL, START_DATE, END_DATE, CSV_FILENAME, DATABASE_URL, TABLE_NAME)