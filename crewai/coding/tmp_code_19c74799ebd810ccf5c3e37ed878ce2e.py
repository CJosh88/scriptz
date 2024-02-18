# Importing required modules
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Define the ticker symbols
tickers = ['NVDA', 'TSLA']

# Get today's date as the end date and the first day of the year as the start date
end = pd.to_datetime('today').date()
start = pd.to_datetime(f'{end.year}-01-01').date()

# Use Yahoo Finance to grab the historical data
data = yf.download(tickers, start=start, end=end)

# Plot the data
data = data['Close']
data.plot(title='NVDA & TSLA Stock Price Change YTD')

# Show the plot
plt.show()