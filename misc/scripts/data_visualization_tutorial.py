#%% data_visualization_tutorial.py, requires you to have data inside your data/misc/tutorials folder, generate using data_pipeline_tutorial.py
import os
import sys
# This line gets the directory where the current file is located
current_file_directory = os.path.dirname(__file__)

# Get the parent parent directory of the current script's directory
parent_directory = os.path.abspath(os.path.join(current_file_directory, os.pardir, os.pardir))

# Define the path to the "data" subfolder within the parent directory
data_directory = os.path.join(parent_directory, "data", "misc", "tutorials")

# Now, append the parent and data directory to sys.path
sys.path.append(data_directory)
sys.path.append(parent_directory)

from src.visualization.visualize import visualize_close_prices
#%%
def main():
    # Configuration
    CSV_FILENAME = os.path.join(data_directory, "S&P_stock_data.csv") # Adjust the filename/path as necessary
    
    # Ensure the CSV file exists before attempting to visualize
    if not os.path.exists(CSV_FILENAME):
        print(f"CSV file '{CSV_FILENAME}' not found. Please check the file path.")
        return
    
    # Call the visualization function
    visualize_close_prices(CSV_FILENAME)

if __name__ == "__main__":
    main()