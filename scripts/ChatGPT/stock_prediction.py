#!/usr/bin/python

import stock_constants
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM


class STOCK_PREDICTION:
    def __init__(self, i_stock, i_df):
        self.stock = i_stock
        self.df = i_df
        self.master_list = []
        self.action = self.stock_prediction()


    def stock_prediction(self):

        # This will be used to determine if the AI models are worth depending on
        i_score_sell = 0
        i_score_buy = 0

        self.master_list.insert(-1, ['RNN', self.RNN()])
        self.master_list.insert(-1, ['ANN', self.ANN()])

        for i in range(len(self.master_list)):
            i_rmse = self.master_list[i][1][0]
            i_sharpe_ratio = self.master_list[i][1][1]
            if i_rmse < 5:
                if i_sharpe_ratio < 0.4:
                    i_score_sell += 1
                else: #i_sharpe_ratio >= 0.4
                    i_score_buy += 1

        if i_score_sell >= 2:
            return stock_constants.STOCK_SELL
        elif i_score_buy >= 2:
            return stock_constants.STOCK_BUY
        else:
            return stock_constants.STOCK_LEAVE

    # Recurrent Neural Networks (RNNs)
    def RNN(self):

        # THis is the number of days the prediction is based on
        seq_len = 30

        # Create a copy of df to prevent overwrite
        df = self.df.copy(deep=True)

        # Preprocess the data
        data = df.filter(['Close']).values
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(data)

        # Split the data into training and testing sets
        training_data_len = math.ceil(len(scaled_data) * .8)
        train_data = scaled_data[0:training_data_len, :]
        x_train = []
        y_train = []

        for i in range(60, len(train_data)):
            x_train.append(train_data[i - seq_len:i, 0])
            y_train.append(train_data[i, 0])

        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        # Build the RNN model
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        model.add(tf.keras.layers.LSTM(50, return_sequences=False))
        model.add(tf.keras.layers.Dense(25))
        model.add(tf.keras.layers.Dense(1))

        # Train the RNN model
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(x_train, y_train, batch_size=32, epochs=10)

        # Test the RNN model
        test_data = scaled_data[training_data_len - seq_len:, :]
        x_test = []
        y_test = data[training_data_len:, :]

        for i in range(seq_len, len(test_data)):
            x_test.append(test_data[i - seq_len:i, 0])

        x_test = np.array(x_test)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

        predictions_scaled = model.predict(x_test)
        predictions = scaler.inverse_transform(predictions_scaled)

        # Calculate the RMSE. Both formulae generates the same result
        rmse = math.sqrt(mean_squared_error(y_test, predictions))
        rmse = np.sqrt(np.mean(((predictions - y_test) ** 2)))

        # Calculate the Sharpe ratio
        mean_return = self.df['Close'].pct_change().mean()
        volatility = self.df['Close'].pct_change().std()
        sharpe_ratio = (mean_return/volatility)

        return [rmse, sharpe_ratio]

    # Artifical Neural Network
    def ANN(self):
        # Create a copy of df to prevent overwrite
        df = self.df.copy(deep=True)

        # THis is the number of days the prediction is based on
        seq_len = 30

        # Prepare the data
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(self.df['Close'].values.reshape(-1, 1))

        # Split the data into training and testing sets
        training_data_len = int(len(scaled_data) * 0.8)
        train_data = scaled_data[0:training_data_len, :]
        test_data = scaled_data[training_data_len:, :]

        # Define the training data
        X_train = []
        y_train = []
        for i in range(seq_len, len(train_data)):
            X_train.append(train_data[i - seq_len:i, 0])
            y_train.append(train_data[i, 0])
        X_train, y_train = np.array(X_train), np.array(y_train)
        X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

        # Build the model
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50))
        model.add(Dropout(0.2))
        model.add(Dense(units=1))

        # Compile the model
        model.compile(optimizer='adam', loss='mean_squared_error')

        # Train the model
        model.fit(X_train, y_train, epochs=10, batch_size=32)

        # Test the model
        X_test = []
        y_test = []
        for i in range(seq_len, len(test_data)):
            X_test.append(test_data[i - seq_len:i, 0])
            y_test.append(test_data[i, 0])
        X_test, y_test = np.array(X_test), np.array(y_test)
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        predicted_stock_price_scaled = model.predict(X_test)
        predicted_stock_price = scaler.inverse_transform(predicted_stock_price_scaled)

        # Calculate the root mean squared error
        #rmse = math.sqrt(mean_squared_error(y_test, predicted_stock_price_scaled)) #Shouldn't use scaled prices
        rmse = math.sqrt(mean_squared_error(df['Close'][training_data_len + seq_len:], predicted_stock_price))

        # Calculate the Sharpe ratio based on the Actual prediction
        mean_return = df['Close'][training_data_len + seq_len:].pct_change().mean()
        volatility = df['Close'][training_data_len + seq_len:].pct_change().std()
        sharpe_ratio_actual = (mean_return / volatility)

        df_predicted = pd.DataFrame(predicted_stock_price)
        mean_return = df_predicted.pct_change().mean()[0]
        volatility = df_predicted.pct_change().std()[0]
        sharpe_ratio_predicted = (mean_return / volatility)

        # Visualize the results
        #plt.plot(df['Close'][training_data_len:])
        #plt.plot(df['Close'][training_data_len + seq_len:].index, predicted_stock_price)
        #plt.legend(['Actual', 'Predicted'])
        #plt.show()
        return [rmse, sharpe_ratio_predicted]