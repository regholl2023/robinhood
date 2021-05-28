#!/usr/bin/python


##############################################################################
#
# This file is the main file. It will pull stock prices from the web
# and generate expected results, along with suggestion on which stocks
# to buy and which to sell
#
##############################################################################

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

# Raw Package
import numpy as np
import pandas as pd
# Data Source
import yfinance as yf
# Data viz
import plotly.graph_objs as go
import requests

# ---------Set sys.path for MAIN execution---------------------------------------
full_path = os.path.abspath(os.path.dirname(sys.argv[0])).split('robinhood')[0]
full_path += "robinhood"
sys.path.append(full_path)
# Walk path and append to sys.path
for root, dirs, files in os.walk(full_path):
    for dir in dirs:
        sys.path.append(os.path.join(root, dir))

import stock_constants
import stock
import ML


def usage():
    print("Usage: Please provide which stocks to process. Defaults to the top 100 stocks")
    print("Example: python scripts/Main.py")
    print("Example: python scripts/Main.py --all")
    print("Example: python scripts/Main.py --top_100")


def main(argv):
    i_stock_list = stock_constants.i_short_list

    for i in range(len(argv)):
        if argv[i] == '--all':
            i_stock_list = []
            API_key = 'c2ohmu2ad3i8sitm0i1g' # Taken from https://finnhub.io/dashboard
            r = requests.get('https://finnhub.io/api/v1/stock/symbol?exchange=US&token=' + API_key)
            r = r.json()
            for i in range(len(r)):
                stock_type = r[i]['type']
                # Only consider Common stocks and ETP and ignore all other types of stocks
                if stock_type == 'Common Stock':
                    i_stock_list.append(r[i]['symbol'])
        elif argv[i] == '--top_100':
            i_stock_list = stock_constants.i_interesting_stocks
        else:
            i_stock_list = stock_constants.i_short_list

    i_base_directory = os.path.abspath(os.path.dirname(sys.argv[0])).split('robinhood')[0]
    i_log_directory = i_base_directory + "robinhood" + "/" + "logs" + "/"

    # Periods can be following
    # 1 week -> 1wk
    # 1 month -> 1mo
    # 1 day -> 1d
    # 1 hour -> 1h
    # 1 min -> 1 m
    stocks = []
    raw_data = []
    print("Start pulling in stock prices")
    for i in range(len(i_stock_list)):

        # It is possible that the listed company no longer exists now.
        # Therefore check it attributes and then skip it if needed
        ticker_object = yf.Ticker(i_stock_list[i])
        if (('regularMarketPrice' not in ticker_object.info) or ('market' not in ticker_object.info)
                or ('exchange' not in ticker_object.info)):
            continue
        else:
            i_exchange = ticker_object.info['exchange']
            i_market = ticker_object.info['market']
            if i_market != 'us_market':
                continue


        # Load historial data for this particular company
        data = yf.download(tickers=i_stock_list[i], period='12mo', interval='1d')
        data.to_csv(i_log_directory + i_stock_list[i] + '.csv')
        raw_data.append(data)

        # Start buying/selling analysis
        stocks.append(stock.STOCK(i_stock_list[i], i_log_directory + i_stock_list[i] + '.csv'))

    #print("Start Machine Learning Algorithms")
    #for i in range(len(i_stock_list)):
    #    ML.ML(raw_data[i], stocks[i])
    #print("Finished")


if __name__ == "__main__":
    main(sys.argv[1:])
