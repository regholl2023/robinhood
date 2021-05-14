#!/usr/bin/python

import sys
import logging
import time
import string
import datetime
import random
import subprocess
import utils


class STOCK:
    def __init__(self, i_name, i_file):
        self.name = i_name
        self.DATE = []
        self.OPEN = []
        self.HIGH = []
        self.LOW = []
        self.CLOSE = []
        self.ADJ_CLOSE = []
        self.VOLUME = []
        self.data = utils.read_CSV(i_file)
        self.process_data()

        # MISC values
        self.highest_stock_value = 0
        self.lowest_stock_value = 0
        self.current_stock_value = 0
        self.weighted_average = 0
        self.process_misc_data()

        # Make predictions/suggestions
        self.recommend_buying()
        self.recommend_selling()

    def recommend_buying(self):
        i_percentage_change = ((self.current_stock_value - self.weighted_average) / (self.weighted_average)) * 100
        if i_percentage_change < -25:
            print("\n===================================================")
            print("We recommend buying the following share: " + self.name)
            print("Historic High: $" + str(self.highest_stock_value))
            print("Historic Low: $" + str(self.lowest_stock_value))
            print("Weighted Average: $" + str(self.weighted_average))
            print("Current Price: $" + str(self.current_stock_value))
            print("Percentage Change = " + str(i_percentage_change) + "%")
            print("===================================================\n")

    def recommend_selling(self):
        i_percentage_change = ((self.weighted_average - self.weighted_average) / (self.weighted_average)) * 100
        if i_percentage_change > 20:
            print("\n===================================================")
            print("We recommend selling the following share: " + self.name)
            print("Historic High: $" + str(self.highest_stock_value))
            print("Historic Low: $" + str(self.lowest_stock_value))
            print("Weighted Average: $" + str(self.weighted_average))
            print("Current Price: $" + str(self.current_stock_value))
            print("Percentage Change = " + str(i_percentage_change) + "%")
            print("===================================================\n")

    def process_misc_data(self):
        self.highest_stock_value = max(self.HIGH,key=lambda x:float(x))
        self.lowest_stock_value = min(self.LOW,key=lambda x:float(x))
        self.current_stock_value = (self.HIGH[-1] + self.LOW[-1]) / 2

        # Calculate the weighted average based on OPENING and CLOSING value
        for i in range(len(self.OPEN)):
            self.weighted_average += self.OPEN[i]/float(len(self.OPEN))

    def process_data(self):
        for i in range(1, len(self.data)):
            self.DATE.append(self.data[i][0])
            self.OPEN.append(float(self.data[i][1]))
            self.HIGH.append(float(self.data[i][2]))
            self.LOW.append(float(self.data[i][3]))
            self.CLOSE.append(float(self.data[i][4]))
            self.ADJ_CLOSE.append(float(self.data[i][5]))
            self.VOLUME.append(float(self.data[i][6]))