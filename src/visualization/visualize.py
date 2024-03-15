import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

def visualize_close_prices(csv_filename):
    """
    Loads stock data from a CSV file, reads the symbol column,
    and visualizes the closing prices over time for that symbol with a light grey background.
    
    Parameters:
    - csv_filename (str): The path to the CSV file containing the stock data.
    """
    # Load the data
    data = pd.read_csv(csv_filename)
    
    # Extract the symbol
    symbol = data['symbol'].iloc[0].upper()
    
    # Convert 'date' column to datetime
    data['date'] = pd.to_datetime(data['date'])
    
    # Set the plot style to default and then customize for light grey background
    plt.style.use('default')
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('#D3D3D3')  # Light grey background for the figure
    ax.set_facecolor('#D3D3D3')  # Light grey background for the axes
    
    ax.plot(data['date'], data['close'], color='teal', label='Close Price')  # Teal for contrast
    
    # Set title and labels with darker font color for contrast
    ax.set_title(f'Closing Prices Over Time for {symbol}', color='black')
    ax.set_xlabel('Date', color='black')
    ax.set_ylabel('Close Price', color='black')
    
    # Format the date on the x-axis for better readability
    date_form = DateFormatter("%Y-%m")
    ax.xaxis.set_major_formatter(date_form)
    
    # Customize the ticks for better readability
    ax.tick_params(axis='x', colors='black')
    ax.tick_params(axis='y', colors='black')
    
    # Customize the legend
    ax.legend()

    # Show grid with a darker color for contrast against light background
    ax.grid(True, color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
    
    # Show the plot
    plt.show()


if __name__ == "__main__":
    visualize_close_prices('S&P_stock_data.csv')