#!/usr/bin/python


##############################################################################
#
# This file is used to pull stock market data from the web and into the
# log directory.
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

import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import REST, TimeFrame

# Raw Package
#import numpy as np
#import pandas as pd
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
#import ML


def usage():
    print("Usage: Please provide which stocks to process. Defaults to the top 100 stocks")
    print("Example: python scripts/Get_Data.py")
    print("Example: python scripts/Get_Data.py --all")
    print("Example: python scripts/Get_Data.py --top_100")


def main(argv):

    # By Default get the short list of stock names
    i_stock_list = stock_constants.i_short_list

    for i in range(len(argv)):
        if argv[i] == '--all':
            i_stock_list = []
            API_key = 'c2ohmu2ad3i8sitm0i1g' # Taken from https://finnhub.io/dashboard
            r = requests.get('https://finnhub.io/api/v1/stock/symbol?exchange=US&token=' + API_key)
            r = r.json()
            for j in range(len(r)):
                print("Processing logs for " + str(r[j]['displaySymbol']))
                stock_type = r[j]['type']
                # Only consider Common stocks and ignore all other types of stocks
                if stock_type == 'Common Stock':
                    # It is possible that the listed company no longer exists now.
                    # Therefore check it attributes and then skip it if needed
                    ticker_object = yf.Ticker(r[j]['symbol'])
                    try:
                        if ticker_object.fast_info is None:
                            continue
                        elif (('last_price' not in ticker_object.fast_info) or ('exchange' not in ticker_object.fast_info)):
                            continue
                        elif 'last_price' in ticker_object.fast_info:
                            i_lastprice = ticker_object.fast_info['last_price']
                            if i_lastprice < 2:
                                continue
                        else:
                            ticker_object.fast_info['last_price']
                    except Exception as e:
                        print("Warning: " + str(e) + ". Continuing......")
                        continue


                        # Don't select the following stocks:
                        #      1) PNK -> Pink Sheet stocks (Rolls Royce is PNK)
                        # if i_exchange == 'PNK':
                        #    continue

                    # Add the remaining stocks to the master stock list
                    i_stock_list.append(r[j]['symbol'])

        elif argv[i] == '--big_list':
            i_stock_list = stock_constants.i_big_list_stocks

        elif argv[i] == '--top_100':
            i_stock_list = stock_constants.i_interesting_stocks_by_symbol

        elif argv[i] == '--alpaca':
            l_approved_exchanges = ['NASDAQ', 'NYSE']
            i_alpaca_object = tradeapi.REST('PKCSBUUOKJN32C5LN716', 'aR9GddDWEcfgRHXUPOUtP6X7YI46JNOJsDUaFUBl',
                                      base_url='https://paper-api.alpaca.markets')
            i_master_list = i_alpaca_object.list_assets(asset_class='us_equity', status='active')
            i_short_list = []
            for i in range(len(i_master_list)):
                if i_master_list[i].exchange in l_approved_exchanges:
                    if i_master_list[i].fractionable:
                        i_shortName = i_master_list[i].symbol
                        try:
                            i_price = (yf.Ticker(i_shortName)).history(period='1d')['Close'][0]
                        except Exception as e:
                            print("Stock: " + i_shortName + ". Warning: " + str(e) + ". Continuing......")
                            continue
                        # Only pick stocks that have a price point of >= $250
                        if i_price >= 250:
                            i_short_list.append(i_master_list[i])
                            i_stock_list.append(i_shortName)

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
        # Load historial data for this particular company
        try:
            data = yf.download(tickers=i_stock_list[i], period='48mo', interval='1d')
            data.to_csv(i_log_directory + i_stock_list[i] + '.csv')
        except Exception as e:
            print("Some error has occured. Continue!!!!!")
            print(e)

    print("Finished get all the required stock logs")



if __name__ == "__main__":
    main(sys.argv[1:])
