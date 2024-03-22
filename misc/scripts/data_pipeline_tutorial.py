import datetime
import os
from sqlalchemy import create_engine
from src.data.fetch_data import fetch_stock_data
from src.data.process_data import prepare_data, clean_data
from src.features.build_features import build_features
from src.data.save_data import save_data_to_csv, save_data_to_db

# This line gets the directory where the current file is located
current_file_directory = os.path.dirname(__file__)

# Get the parent parent directory of the current script's directory
parent_directory = os.path.abspath(os.path.join(current_file_directory, os.pardir, os.pardir))

# Define the path to the "data" subfolder within the parent directory
data_directory = os.path.join(parent_directory, "data", "misc", "tutorials")

# Ensure the target directory exists
os.makedirs(data_directory, exist_ok=True)

CSV_FILENAME = os.path.join(data_directory, "S&P_stock_data.csv")
DATABASE_URL = f"sqlite:///{os.path.join(data_directory, 'S&P_stock_data.db')}"

# Configuration
TICKER_SYMBOL = "^GSPC"
START_DATE = "2000-01-01"
END_DATE = datetime.datetime.now().strftime('%Y-%m-%d')
TABLE_NAME = "stock_data"

def run_data_pipeline(ticker_symbol, start_date, end_date, csv_filename, database_url, table_name):
    # Fetch stock data
    print(f"Fetching data for {ticker_symbol} from {start_date} to {end_date}...")
    data = fetch_stock_data(ticker_symbol, start_date, end_date)

    # Run through preprocessing before splitting
    dataFull = clean_data(data) # Clean raw data
    dataFull = build_features(dataFull) # Add features

    # Save the processed full data to a CSV file
    print(f"Saving full data to {csv_filename}...")
    save_data_to_csv(dataFull, csv_filename)
    
    # Process the data into training
    print("Processing training data...")
    train_data, _ = prepare_data(data,0.1)

    # Split the filename from its extension
    filename, file_extension = os.path.splitext(csv_filename)

    # Append "_train" to the filename and reattach the extension
    train_csv_filename = f"{filename}_train{file_extension}"
    
    # Save the processed training data to a CSV file
    print(f"Saving data to {train_csv_filename}...")
    save_data_to_csv(train_data, train_csv_filename)
    
    # Save the processed training data to a database
    print(f"Saving data to database {database_url}, table {table_name}...")
    save_data_to_db(train_data, database_url, table_name)
    
    print("Data pipeline completed successfully.")

if __name__ == "__main__":
    run_data_pipeline(TICKER_SYMBOL, START_DATE, END_DATE, CSV_FILENAME, DATABASE_URL, TABLE_NAME)