#!/usr/bin/python
import pandas as pd
import numpy as np
import math
import alpaca_trade_api as tradeapi

from alpaca_trade_api.rest import REST, TimeFrame
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense


# Set up the Alpaca API
api = tradeapi.REST('PKCSBUUOKJN32C5LN716', 'aR9GddDWEcfgRHXUPOUtP6X7YI46JNOJsDUaFUBl',
                    base_url='https://paper-api.alpaca.markets')

# Set the stock symbol and time frame
symbol = 'AAPL'
start_date = '2016-01-01'
end_date = '2023-04-24'

# Get the historical data
data = api.get_bars(symbol, TimeFrame.Day, start_date, end_date).df

# Save the data as a CSV file
data.to_csv('AAPL.csv')



# Load the data from the CSV file
data = pd.read_csv('AAPL.csv')


# Load the CSV data into a pandas dataframe
df = pd.read_csv(f'AAPL.csv')

print(df.head())

# Define the features and target
X = np.array(df['open']).reshape(-1, 1)
y = np.array(df['close'])

# Split the data into training and testing sets
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Train a linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculate the root mean squared error
rmse = math.sqrt(mean_squared_error(y_test, y_pred))

# Calculate the mean return and volatility of the stock
mean_return = df['close'].pct_change().mean()
volatility = df['close'].pct_change().std()

# Calculate the Sharpe ratio
sharpe_ratio = (mean_return / volatility) * math.sqrt(252)

# Print the results
print(f'RMSE: {rmse:.2f}')
print(f'Sharpe Ratio: {sharpe_ratio:.2f}')