#%%
import yfinance as yf

# Fetch historical data for Apple Inc.
ticker = yf.Ticker("AAPL")
hist = ticker.history(period="max")  # You can customize the period

# Do something with the data
print(hist.head())