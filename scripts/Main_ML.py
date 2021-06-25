#!/usr/bin/python


##############################################################################
#
# This file is used to pull perform machine learning on stock data from a given directory.
# This script needs a folder that has the .csv files within it to be able to process/analyse data.
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
import glob

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
    print("Usage: Please provide the directory where <stock>.csv files are stored."
          "Defaults to the log folder within the current directory")
    print("Example: python scripts/Main_ML.py")
    print("Example: python scripts/Main_ML.py --<location>")

def main(argv):

    if len(argv) > 1:
        print("Please provide only one directory")
        raise Exception
    elif len(argv) == 1:
        i_log_directory = argv[0]
    else:
        i_base_directory = os.path.abspath(os.path.dirname(sys.argv[0])).split('robinhood')[0]
        i_log_directory = i_base_directory + "robinhood" + "/" + "logs" + "/"

    # Get a list of all files from the log directory
    i_stocks_list = os.listdir(i_log_directory)
    for i_stock in i_stocks_list:

        # Only process the csv files
        if i_stock.endswith(".csv"):
            # These logs are important in determining if the process
            # is continuing or is getting stuck for some reason
            print("\n\nProcessing " + i_stock)
            sys.stdout.flush()
            ML.ML1(i_log_directory + i_stock)


if __name__ == "__main__":
    main(sys.argv[1:])
