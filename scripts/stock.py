#!/usr/bin/python

import sys
import logging
import time
import string
import datetime
import random
import subprocess
import utils
import urllib
import json
import yfinance as yf
import stock_constants
import sim_logging
import requests
from scipy.stats import linregress
from urllib.error import HTTPError

class STOCK:
    def __init__(self, i_name, i_file):
        self.simlog = sim_logging.SIMLOG(log_dir=i_file.rsplit('/', 1)[0])
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
            self.simlog.error("Unable to get stock data from csv file. Skipping!!!")
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
        self.ExchDisp = ''

        try:
            time.sleep(1)
            self.ticker_object = yf.Ticker(i_name)

            # No need to process any data if there is no information on this stock
            if self.ticker_object.fast_info is None:
                self.simlog.error("Unable to get the ticker_object.fast_info. Skipping!!!")
                return

            response = urllib.request.urlopen(f'https://query2.finance.yahoo.com/v1/finance/search?q={i_name}')
            content = response.read()

            if 'shortname' in json.loads(content.decode('utf8'))['quotes'][0]:
                self.shortName = json.loads(content.decode('utf8'))['quotes'][0]['shortname']
                self.simlog.debug("shortName is " + str(self.shortName))

            if 'longname' in json.loads(content.decode('utf8'))['quotes'][0]:
                self.longName = json.loads(content.decode('utf8'))['quotes'][0]['longname']
                self.simlog.debug("longName is " + str(self.shortName))

            if 'sector' in json.loads(content.decode('utf8'))['quotes'][0]:
                self.sector = json.loads(content.decode('utf8'))['quotes'][0]['sector']
                self.simlog.debug("sector is " + str(self.sector))

            if 'industry' in json.loads(content.decode('utf8'))['quotes'][0]:
                self.industry = json.loads(content.decode('utf8'))['quotes'][0]['industry']
                self.simlog.debug("industry is " + str(self.industry))

            if 'exchDisp' in json.loads(content.decode('utf8'))['quotes'][0]:
                self.ExchDisp = json.loads(content.decode('utf8'))['quotes'][0]['exchDisp']
                self.simlog.debug("ExchDisp is " + str(self.ExchDisp))

            if 'exchange' in self.ticker_object.fast_info:
                self.exchange = self.ticker_object.fast_info['exchange']
                self.simlog.debug("exchange is " + str(self.exchange))

            if 'last_price' not in self.ticker_object.fast_info:
                self.simlog.error("Unable to get the regularMarketPrice. Skipping!!!")
                return
            else:
                self.regularMarketPrice = self.ticker_object.fast_info['last_price']
                self.simlog.debug("regularMarketPrice is " + str(self.regularMarketPrice))

        except urllib.error.HTTPError as e:
            self.simlog.warning(str(e))
            self.simlog.warning("Skipping......")
            return

        except IndexError as e:
            self.simlog.warning(str(e))
            self.simlog.warning("Skipping.........")
            return

        except Exception as e:
            print(e)
            raise Exception

        # MISC values
        self.highest_stock_value = 0
        self.lowest_stock_value = 0
        self.current_stock_value = 0
        self.weighted_average = 0
        self.process_misc_data()
        self.get_misc_data()

        # Make predictions/suggestions
        self.recommend_buying()
        self.recommend_selling()

    def recommend_buying(self):
        try:
            if (self.weighted_average == 0) or (self.lowest_stock_value == 0) or (self.highest_stock_value == 0) or (
                    self.weighted_average is None) or (self.lowest_stock_value is None) or (
                    self.highest_stock_value is None) or (self.current_stock_value is None):
                self.simlog.debug(
                    "Unable to get one of the following values: weighted_average/lowest_stock_value/highest_stock_value")
                return
            else:
                i_percentage_change = ((self.current_stock_value - self.weighted_average) / (
                    self.weighted_average)) * 100
                self.simlog.debug("percentage_change = " + str(i_percentage_change) + "%")

                i_percentage_difference_from_highest = ((self.current_stock_value - self.highest_stock_value) /
                                                        self.highest_stock_value) * 100
                self.simlog.debug(
                    "percentage_difference_from_highest = " + str(i_percentage_difference_from_highest) + "%")

                i_percentage_difference_from_lowest = ((self.current_stock_value - self.lowest_stock_value) /
                                                       self.lowest_stock_value) * 100
                self.simlog.debug(
                    "percentage_difference_from_lowest = " + str(i_percentage_difference_from_lowest) + "%")

                if ((i_percentage_change < -25) and (i_percentage_difference_from_lowest < 1)) or \
                        ((i_percentage_change < -20) and (i_percentage_difference_from_lowest < 25) and (
                                self.name in stock_constants.i_interesting_stocks)):
                    self.simlog.info("===================================================")
                    self.simlog.info("===================================================")
                    self.simlog.info("===================================================")
                    self.simlog.info("===================================================")
                    self.simlog.info(
                        "We recommend buying the following share: " + self.shortName + "(" + self.name + ")")

                    # Wrap it with try/catch statement because it is not re-creatable in pycharm
                    try:
                        if self.sector is not None:
                            self.simlog.info("Sector = " + str(self.sector))
                        if self.industry is not None:
                            self.simlog.info("Industry = " + str(self.industry))
                    except Exception as e:
                        self.simlog.warning("Unable to get sector or industry value")
                        pass

                    self.simlog.info("Exchange= " + self.exchange)
                    self.simlog.info("ExchDisp= " + self.ExchDisp)
                    self.simlog.info("Historic High: $" + str(self.highest_stock_value))
                    self.simlog.info("Historic Low: $" + str(self.lowest_stock_value))
                    self.simlog.info("Weighted Average: $" + str(self.weighted_average))
                    self.simlog.info("Current Price: $" + str(self.current_stock_value))
                    self.simlog.info("Slope is equal to " + str(self.slope.slope))
                    self.simlog.info("Percentage Difference from average = " + str(i_percentage_change) + "%")
                    self.simlog.info(
                        "Percentage Difference from highest = " + str(i_percentage_difference_from_highest) + "%")
                    self.simlog.info(
                        "Percentage Difference from lowest = " + str(i_percentage_difference_from_lowest) + "%")
                    self.simlog.info("Price to Earnings (P/E) ratio = " + str(self.PERatio) +
                                     "; if < 15 stock is considered undervalued, while > 25 is considered overvalued")
                    self.simlog.info("Price/Earnings to Growth (PEG) ratio = " + str(self.PEGRatio) +
                                     "; 1 = fairly valued; < 1 undervalued; > 1 overvalued")
                    self.simlog.info("Price to Book (P/B) ratio = " + str(self.PriceToBookRatio) +
                                     "; if < 1 stock is considered undervalued, while > 3 is considered overvalued")
                    self.simlog.info("Divident yeild = " + str(self.DividendYield))
                    self.simlog.info("===================================================")
                    self.simlog.info("===================================================")
                    self.simlog.info("===================================================")
                    self.simlog.info("===================================================\n\n\n")

                    # We need to create a file in the log directory that has
                    # our the recommendations to buy. Stocks must have the following attributes
                    # Current Price over $10
                    # Slope is positive
                    if (self.slope.slope > 0) and (self.current_stock_value > 10):
                        file_object = open(self.file.rsplit('/', 3)[0] + '/blog/recommendations.txt', 'a+')
                        file_object.write("BUY:\n")
                        file_object.write("stockName = " + self.name + '\n')
                        file_object.write("longName = " + self.longName + '\n')
                        file_object.write("sector = " + self.longName + '\n')
                        file_object.write("industry = " + self.longName + '\n')
                        file_object.write("slope = " + str(self.slope.slope) + '\n')
                        file_object.write("regularMarketPrice = " + str(self.regularMarketPrice) + '\n')
                        file_object.write("lowest_stock_value = " + str(self.lowest_stock_value) + '\n')
                        file_object.write("highest_stock_value = " + str(self.highest_stock_value) + '\n')
                        file_object.write("weighted_average = " + str(self.weighted_average) + '\n')
                        file_object.write("Price to Earnings (P/E) ratio = " + str(self.PERatio) +
                                         "; if < 15 stock is considered undervalued, while > 25 is considered overvalued\n")
                        file_object.write("Price/Earnings to Growth (PEG) ratio = " + str(self.PEGRatio) +
                                         "; 1 = fairly valued; < 1 undervalued; > 1 overvalued\n")
                        file_object.write("Price to Book (P/B) ratio = " + str(self.PriceToBookRatio) +
                                         "; if < 1 stock is considered undervalued, while > 3 is considered overvalued\n")
                        file_object.write("Divident yeild = " + str(self.DividendYield) + "/n")
                        file_object.write("\n\n")
                        file_object.close()

        except Exception as e:
            print(e)
            raise Exception

    def recommend_selling(self):
        try:
            # Skip the stock if the weighted average is 0
            if ((self.weighted_average == 0) or (self.lowest_stock_value == 0) or (self.highest_stock_value == 0) or (
                    self.weighted_average is None) or (self.lowest_stock_value is None) or (
                    self.highest_stock_value is None) or (self.current_stock_value is None) or (
                    self.name not in stock_constants.i_stocks_i_own)):
                self.simlog.debug(
                    "Unable to get one of the following values: weighted_average/lowest_stock_value/highest_stock_value")
                return
            else:
                i_percentage_change = ((self.current_stock_value - self.weighted_average) / (
                    self.weighted_average)) * 100
                i_percentage_difference_from_highest = ((self.current_stock_value - self.highest_stock_value) / (
                    self.highest_stock_value)) * 100
                i_percentage_difference_from_lowest = ((self.current_stock_value - self.lowest_stock_value) / (
                    self.lowest_stock_value)) * 100
                if (i_percentage_change > 25) and (i_percentage_difference_from_highest < 20):
                    self.simlog.info("===================================================")
                    self.simlog.info("===================================================")
                    self.simlog.info("===================================================")
                    self.simlog.info("===================================================")
                    self.simlog.info(
                        "We recommend selling the following share: " + self.shortName + "(" + self.name + ")")
                    if self.sector is not None:
                        self.simlog.info("Sector= " + self.sector)
                    if self.industry is not None:
                        self.simlog.info("Industry= " + self.industry)
                    self.simlog.info("Exchange= " + self.exchange)
                    self.simlog.info("ExchDisp= " + self.ExchDisp)
                    self.simlog.info("Historic High: $" + str(self.highest_stock_value))
                    self.simlog.info("Historic Low: $" + str(self.lowest_stock_value))
                    self.simlog.info("Weighted Average: $" + str(self.weighted_average))
                    self.simlog.info("Current Price: $" + str(self.current_stock_value))
                    self.simlog.info("Slope is equal to " + str(self.slope.slope))
                    self.simlog.info("Percentage Difference from average = " + str(i_percentage_change) + "%")
                    self.simlog.info(
                        "Percentage Difference from highest = " + str(i_percentage_difference_from_highest) + "%")
                    self.simlog.info(
                        "Percentage Difference from lowest = " + str(i_percentage_difference_from_lowest) + "%")
                    self.simlog.info("Price to Earnings (P/E) ratio = " + str(self.PERatio) +
                                     "; if < 15 stock is considered undervalued, while > 25 is considered overvalued")
                    self.simlog.info("Price/Earnings to Growth (PEG) ratio = " + str(self.PEGRatio) +
                                     "; 1 = fairly valued; < 1 undervalued; > 1 overvalued")
                    self.simlog.info("Price to Book (P/B) ratio = " + str(self.PriceToBookRatio) +
                                     "; if < 1 stock is considered undervalued, while > 3 is considered overvalued")
                    self.simlog.info("Divident yeild = " +str(self.DividendYield))
                    self.simlog.info("===================================================")
                    self.simlog.info("===================================================")
                    self.simlog.info("===================================================")
                    self.simlog.info("===================================================\n\n\n")
        except Exception as e:
            print(e)
            raise Exception


    def get_misc_data(self):
        api_key = '4HXSW88OCUXENZYN'

        try:
            i_response_overview = requests.get(
                f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={self.name}&apikey={api_key}')
            self.PERatio = i_response_overview.json()['PERatio']
            self.PEGRatio = i_response_overview.json()['PEGRatio']
            self.PriceToBookRatio = i_response_overview.json()['PriceToBookRatio']
            self.DividendYield = i_response_overview.json()['DividendYield']
            #self.DebtToEquityRatio = i_response_overview.json()['DebtToEquityRatio']
            self.MarketCapitalization = i_response_overview.json()['MarketCapitalization']
            #self.EarningsGrowth = i_response_overview.json()['EarningsGrowth']  # Doesn't exist
        except Exception as e:
            self.simlog.warning("Failed to get misc data for stock")
            self.simlog.warning(str(e))



    @staticmethod
    def get_data_from_alphavantage(i_symbol):
        api_key = '4HXSW88OCUXENZYN'
        response = requests.get(f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={i_symbol}&apikey={api_key}')
        return response

    def process_misc_data(self):
        self.highest_stock_value = max(self.HIGH, key=lambda x: float(x))
        self.lowest_stock_value = min(self.LOW, key=lambda x: float(x))
        self.current_stock_value = self.regularMarketPrice  # (self.HIGH[-1] + self.LOW[-1]) / 2
        self.slope = linregress(self.HIGH, list(range(1, len(self.DATE) + 1)))

        # Calculate the weighted average based on OPENING and CLOSING value
        for i in range(len(self.OPEN)):
            self.weighted_average += self.OPEN[i] / float(len(self.OPEN))

    def process_data(self):
        for i in range(1, len(self.data)):

            # It is possible that one of the entry is empty.
            # Therefore copy the next entry into the current entry
            if self.data[i][1] == '':
                self.data[i] = self.data[i - 1]
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
                    print(e)
                    x = self.data[i][1]
                    raise Exception
