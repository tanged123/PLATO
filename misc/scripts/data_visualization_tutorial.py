#%% data_visualization_tutorial.py
import os
from src.visualization.visualize import visualize_close_prices
#%%
def main():
    # Configuration
    CSV_FILENAME = "S&P_stock_data.csv"  # Adjust the filename/path as necessary
    
    # Ensure the CSV file exists before attempting to visualize
    if not os.path.exists(CSV_FILENAME):
        print(f"CSV file '{CSV_FILENAME}' not found. Please check the file path.")
        return
    
    # Call the visualization function
    visualize_close_prices(CSV_FILENAME)

if __name__ == "__main__":
    main()