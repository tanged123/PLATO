# src/data/save_data.py

import pandas as pd
import uuid
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
    Saves the provided DataFrame to a database table using pandas' to_sql method,
    which automatically handles column names and data types.

    Parameters:
    - data (pandas.DataFrame): The data to save. Assumes column names are already in lowercase.
    - database_url (str): The database URL.
    - table_name (str): The table name where data should be saved.
    """
    engine = create_engine(database_url)
    # Convert UUIDs to strings if not already done
    if 'id' in data.columns and isinstance(data['id'].iloc[0], uuid.UUID):
        data['id'] = data['id'].apply(lambda x: str(x))
    # Use the DataFrame's to_sql method to save data to the database
    data.to_sql(name=table_name, con=engine, index=False, if_exists='append')

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
