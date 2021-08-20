#!/usr/bin/python

import sys
import logging
import time
import string
import datetime
import random
import subprocess
import utils
import yfinance as yf
import stock_constants
from scipy.stats import linregress

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
        self.file = i_file

        # It is possible that the csv file has not data points.
        # So check the len(self.data) and skip this particular stock if no
        # data exists
        if len(self.data) <= 1:
            print("Unable to get stock data from csv file. Skipping!!!")
            return
        else:
            self.process_data()

        self.slope = None
        self.industry = None
        self.sector = None
        self.exchange = ''
        self.market = ''
        self.shortName = ''
        self.longName = ''


        try:
            self.ticker_object = yf.Ticker(i_name)
            if 'shortName' in self.ticker_object.info:
                self.shortName = self.ticker_object.info['shortName']
            if 'longName' in self.ticker_object.info:
                self.longName = self.ticker_object.info['longName']
            if 'sector' in self.ticker_object.info:
                self.sector = self.ticker_object.info['sector']
            if 'industry' in self.ticker_object.info:
                self.industry = self.ticker_object.info['industry']
            if 'market' in self.ticker_object.info:
                self.market = self.ticker_object.info['market']
            if 'exchange' in self.ticker_object.info:
                self.exchange = self.ticker_object.info['exchange']
            if 'regularMarketPrice' not in self.ticker_object.info:
                print("Unable to get the regularMarketPrice. Skipping!!!")
                return
            else:
                self.regularMarketPrice = self.ticker_object.info['regularMarketPrice']

        except Exception as e:
            print(e.msg)
            raise Exception

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
        try:
            if (self.weighted_average == 0) or (self.lowest_stock_value == 0) or (self.lowest_stock_value == 0):
                pass
            else:
                i_percentage_change = ((self.current_stock_value - self.weighted_average)/(self.weighted_average)) * 100
                i_percentage_difference_from_highest = ((self.current_stock_value - self.highest_stock_value)/(self.highest_stock_value)) * 100
                i_percentage_difference_from_lowest = ((self.current_stock_value - self.lowest_stock_value) / (self.lowest_stock_value)) * 100
                if ((i_percentage_change < -25) and (i_percentage_difference_from_lowest < 1)) or \
                        ((i_percentage_change < -20) and (i_percentage_difference_from_lowest < 25) and (self.name in stock_constants.i_interesting_stocks)):
                    print("\n\n\n\n===================================================")
                    print("===================================================\n")
                    print("===================================================\n")
                    print("===================================================\n")
                    print("We recommend buying the following share: " + self.shortName + "(" + self.name + ")")

                    # Wrap it with try/catch statement because it is not re-creatable in pycharm
                    try:
                        if self.sector is not None:
                            print("Sector= " + self.sector)
                        if self.industry is not None:
                            print("Industry= " + self.industry)
                    except Exception as e:
                        pass

                    print("Exchange= " + self.exchange)
                    print("Market= " + self.market)
                    print("Historic High: $" + str(self.highest_stock_value))
                    print("Historic Low: $" + str(self.lowest_stock_value))
                    print("Weighted Average: $" + str(self.weighted_average))
                    print("Current Price: $" + str(self.current_stock_value))
                    print("Slope is equal to " + str(self.slope.slope))
                    print("Percentage Difference from average = " + str(i_percentage_change) + "%")
                    print("Percentage Difference from highest = " + str(i_percentage_difference_from_highest) + "%")
                    print("Percentage Difference from lowest = " + str(i_percentage_difference_from_lowest) + "%")
                    print("===================================================\n")
                    print("===================================================\n")
                    print("===================================================\n")
                    print("===================================================\n\n\n\n")
        except Exception as e:
            print(e.msg)
            raise Exception

    def recommend_selling(self):
        try:
            # Skip the stock if the weighted average is 0
            if (self.weighted_average == 0) or (self.lowest_stock_value == 0) \
                    or (self.lowest_stock_value == 0) or (self.name not in stock_constants.i_stocks_i_own):
                pass
            else:
                i_percentage_change = ((self.current_stock_value - self.weighted_average)/(self.weighted_average)) * 100
                i_percentage_difference_from_highest = ((self.current_stock_value - self.highest_stock_value)/(self.highest_stock_value)) * 100
                i_percentage_difference_from_lowest = ((self.current_stock_value - self.lowest_stock_value)/(self.lowest_stock_value)) * 100
                if (i_percentage_change > 25) and (i_percentage_difference_from_highest < 20):
                    print("\n\n\n\n===================================================")
                    print("===================================================\n")
                    print("===================================================\n")
                    print("===================================================\n")
                    print("We recommend selling the following share: " + self.shortName + "(" + self.name + ")")
                    if self.sector is not None:
                        print("Sector= " + self.sector)
                    if self.industry is not None:
                        print("Industry= " + self.industry)
                    print("Exchange= " + self.exchange)
                    print("Market= " + self.market)
                    print("Historic High: $" + str(self.highest_stock_value))
                    print("Historic Low: $" + str(self.lowest_stock_value))
                    print("Weighted Average: $" + str(self.weighted_average))
                    print("Current Price: $" + str(self.current_stock_value))
                    print("Slope is equal to " + str(self.slope.slope))
                    print("Percentage Difference from average = " + str(i_percentage_change) + "%")
                    print("Percentage Difference from highest = " + str(i_percentage_difference_from_highest) + "%")
                    print("Percentage Difference from lowest = " + str(i_percentage_difference_from_lowest) + "%")
                    print("===================================================\n")
                    print("===================================================\n")
                    print("===================================================\n")
                    print("===================================================\n\n\n\n")
        except Exception as e:
            raise Exception

    def process_misc_data(self):
        self.highest_stock_value = max(self.HIGH,key=lambda x:float(x))
        self.lowest_stock_value = min(self.LOW,key=lambda x:float(x))
        self.current_stock_value = self.regularMarketPrice #(self.HIGH[-1] + self.LOW[-1]) / 2
        self.slope = linregress(self.HIGH, list(range(1, len(self.DATE) + 1)))

        # Calculate the weighted average based on OPENING and CLOSING value
        for i in range(len(self.OPEN)):
            self.weighted_average += self.OPEN[i]/float(len(self.OPEN))

    def process_data(self):
        for i in range(1, len(self.data)):

            # It is possible that one of the entry is empty.
            # Therefore copy the next entry into the current entry
            if self.data[i][1] == '':
                self.data[i] = self.data[i-1]
                pass
            else:
                try:
                    self.DATE.append(self.data[i][0])
                    self.OPEN.append(float(self.data[i][1]))
                    self.HIGH.append(float(self.data[i][2]))
                    self.LOW.append(float(self.data[i][3]))
                    self.CLOSE.append(float(self.data[i][4]))
                    self.ADJ_CLOSE.append(float(self.data[i][5]))
                    self.VOLUME.append(float(self.data[i][6]))
                except Exception as e:
                    x = self.data[i][1]
                    raise Exception
