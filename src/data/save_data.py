# src/data/save_data.py

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class StockData(Base):
    __tablename__ = 'stock_data'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)

def save_data_to_db(data, database_url, table_name='stock_data'):
    """
    Saves the provided DataFrame to a database table using SQLAlchemy.

    Parameters:
    data (pandas.DataFrame): The data to save.
    database_url (str): The database URL.
    table_name (str): The table name where data should be saved.
    """
    # Convert 'Date' column to datetime objects
    data['Date'] = pd.to_datetime(data['Date']).dt.date

    engine = create_engine(database_url)
    Base.metadata.create_all(engine)  # Create the table if it doesn't exist
    Session = sessionmaker(bind=engine)
    session = Session()

    for _, row in data.iterrows():
        # Just before saving to DB, ensure the DataFrame has the expected columns
        expected_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        if not all(column in data.columns for column in expected_columns):
            raise ValueError(f"DataFrame is missing one of the expected columns: {expected_columns}")

        stock_entry = StockData(date=row['Date'], open=row['Open'], high=row['High'], low=row['Low'], close=row['Close'], volume=row['Volume'])
        session.add(stock_entry)

    session.commit()
    session.close()

def save_data_to_csv(data, filename):
    """
    Saves the provided DataFrame to a CSV file.

    Parameters:
    data (pandas.DataFrame): The data to save.
    filename (str): The path to the file where data should be saved.
    """
    data.to_csv(filename, index=False)

# Example usage
if __name__ == "__main__":
    data = pd.DataFrame({
        'Date': ['2020-01-01', '2020-01-02'],
        'Open' : [290, 290],
        'Close': [300, 305],
        'Volume': [1000, 1500],
        'High' : [310, 310],
        'Low' : [290, 290]
    })
    filename = 'stock_data.csv'
    save_data_to_csv(data, filename)

    database_url = 'sqlite:///stock_data.db'  # Example with SQLite
    save_data_to_db(data, database_url)
