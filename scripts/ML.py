#!/usr/bin/env python

import sys
import logging
import time
import string
import datetime
import getopt
import random
import subprocess
import os
import csv
from tabulate import tabulate

# Import Machine Leaning Libraries
#Install the dependencies
import numpy as np
import pandas as pd
from sklearn.svm import SVR
from sklearn.svm import NuSVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
plt.style.use('bmh')


i_global_future_days_to_predict = 60

class ML1:
    def __init__(self, i_stock_file):
        self.df = None
        self.models = [[]]
        self.stock_file = i_stock_file

        self.add_models()
        self.process_data()

    def add_models(self):
        self.models.append(["linear_SVR", SVR(kernel='linear', C=1000.0)])
        self.models.append(["poly_SVR", SVR(kernel='poly', C=1000.0, degree=2)])
        self.models.append(["RBF_SVR", SVR(kernel='rbf', C=10000.0, gamma=0.85)])
        self.models.append(["RBF_NuSVR", NuSVR(kernel='rbf', C=10000.0, gamma=0.85)])
        del self.models[0]

    def process_data(self):
        # Store the Closing value data into a separate variable

        df = pd.read_csv(self.stock_file)

        # Create empty lists
        days = list()
        adj_close_prices = list()

        # Get only the date and the adjusted close prices
        df_days = df.loc[:, 'Date']
        df_adj_close = df.loc[:, 'Adj Close']

        # Create the independent data set (dates)
        for i in range(len(df)):
            days.append([int(i)])

        # Create the independent data set (adj close prices)
        for adj_close_price in df_adj_close:
            adj_close_prices.append(float(adj_close_price))

        mydata = [[]]
        head = ["Model Name", "Yesterday", "Today", "Tomorrow", "1 week", "1 month"]
        # Process all the models one by one
        for i in range(len(self.models)):
            self.models[i][1].fit(days, adj_close_prices)
            mydata.append([self.models[i][0], self.models[i][1].predict([[len(days)]]).item(), self.models[i][1].predict([[len(days) + 1]]).item(),
                           self.models[i][1].predict([[len(days) + 2]]).item(), self.models[i][1].predict([[len(days) + 7]]).item(),
                           self.models[i][1].predict([[len(days) + 30]]).item()])

        del mydata[0]
        print(tabulate(mydata, headers=head, tablefmt="grid"))


class ML:
    def __init__(self, i_raw_data, i_stock):

        df = pd.read_csv(i_stock.file)

        # Visualize the data. I want to see what the closing price of the stocks looks like on a graph.
        #plt.figure(figsize=(16, 8))
        #plt.title('Netflix', fontsize=18)
        #plt.xlabel('Days', fontsize=18)
        #plt.ylabel('Close Price USD ($)', fontsize=18)
        #plt.plot(df['Close'])
        #plt.show()

        df = df[['Close']]

        # Create a variable to predict 'x' days out into the future
        future_days = 30
        # Create a new column (the target or dependent variable) shifted 'x' units/days up
        df['Prediction'] = df[['Close']].shift(-future_days)

        X = np.array(df.drop(['Prediction'], 1))[:-future_days]

        # Create the target data set
        y = np.array(df['Prediction'])[:-future_days]

        # Split the data into 75% training and 25% testing data sets
        x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

        # Create the decision tree regressor model
        tree = DecisionTreeRegressor().fit(x_train, y_train)
        # Create the linear regression model
        lr = LinearRegression().fit(x_train, y_train)

        # Get the feature data,
        # AKA all the rows from the original data set except the last 'x' days
        x_future = df.drop(['Prediction'], 1)[:-future_days]
        # Get the last 'x' rows
        x_future = x_future.tail(future_days)
        # Convert the data set into a numpy array
        x_future = np.array(x_future)

        # Show the model tree prediction
        tree_prediction = tree.predict(x_future)
        # Show the model linear regression prediction
        lr_prediction = lr.predict(x_future)

        # Visualize the data
        predictions = tree_prediction
        # Plot the data
        valid = df[X.shape[0]:]
        valid['Predictions'] = predictions  # Create a new column called 'Predictions' that will hold the pred prices
        plt.figure(figsize=(16, 8))
        plt.title('Model Decision Tree')
        plt.xlabel('Days', fontsize=18)
        plt.ylabel('Close Price USD ($)', fontsize=18)
        plt.plot(valid[['Predictions']])
        plt.plot(df['Close'])
        plt.plot(valid[['Close']])
        #plt.plot(valid[['Close', 'Predictions']])
        plt.legend(['Train', 'Val', 'Prediction'], loc='lower right')
        plt.show()


        # Visualize the data
        predictions = lr_prediction
        # Plot the data
        valid = df[X.shape[0]:]
        valid['Predictions'] = predictions  # Create a new column called 'Predictions' that will hold the pred prices
        plt.figure(figsize=(16, 8))
        plt.title('Model Linear Regression')
        plt.xlabel('Days', fontsize=18)
        plt.ylabel('Close Price USD ($)', fontsize=18)
        plt.plot(df['Close'])
        plt.plot(valid[['Close', 'Predictions']])
        plt.legend(['Train', 'Val', 'Prediction'], loc='lower right')
        plt.show()


        x = 1
