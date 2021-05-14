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
#Data Source
import yfinance as yf
#Data viz
import plotly.graph_objs as go

# ---------Set sys.path for MAIN execution---------------------------------------
full_path = os.path.abspath(os.path.dirname(sys.argv[0])).split('robinhood')[0]
full_path += "robinhood"
sys.path.append(full_path)
# Walk path and append to sys.path
for root, dirs, files in os.walk(full_path):
    for dir in dirs:
        sys.path.append(os.path.join(root, dir))


def main(argv):
    print("Start pulling in stock prices")
    # Periods can be following
    # 1 week -> 1wk
    # 1 month -> 1mo
    # 1 day -> 1d
    # 1 hour -> 1h
    # 1 min -> 1 m
    data = yf.download(tickers='UBER', period='2mo', interval='1d')

    data.to_csv('first_yahoo_prices_volumes_to_csv_demo.csv')

    print("Finished")


if __name__ == "__main__":
    main(sys.argv[1:])