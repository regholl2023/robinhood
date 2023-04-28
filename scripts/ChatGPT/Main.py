#!/usr/bin/python

# This file will either take input a CSV file, or use the existing files located under robinhoold/logs folder.
# Based on the CSV files, it will generate AI models and then calculate the sharpe ratio and RMSE value.
# Using those parameters, we will decide on whether to buy/sell stocks using alpaca API.

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

import pandas as pd

import warnings
warnings.filterwarnings("ignore")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# ---------Set sys.path for MAIN execution---------------------------------------
full_path = os.path.abspath(os.path.dirname(sys.argv[0])).split('robinhood')[0]
full_path += "robinhood"
sys.path.append(full_path)
# Walk path and append to sys.path
for root, dirs, files in os.walk(full_path):
    for dir in dirs:
        sys.path.append(os.path.join(root, dir))

import sim_logging
import stock_constants
from stock_prediction import STOCK_PREDICTION
from alpaca import ALPACA

def usage():
    print("Usage: Provide a path to the csv file. Default is to use all csv files within /logs folder")
    print("Example: python scripts/ChatGPT/Main.py")
    print("Example: python scripts/ChatGPT/Main.py -i /home/saqib/robinhood/logs/AAPL.csv")

def main(argv):
    i_stock_list = []

    i_log_directory = "/tmp/"
    simlog = sim_logging.SIMLOG(log_dir=i_log_directory)

    # Step-0 Get the list of CSV files that needs to be processed
    # No input provided. Look inside /logs folder
    if len(sys.argv) == 1:
        for i_file in os.listdir(full_path + '/logs'):
            if i_file.endswith(".csv"):
                i_stock_list.append(full_path + '/logs/' + i_file)
    # Perhaps the used supplied a csv file. Check
    for i in range(len(argv)):
        # Perhaps the used supplied a csv file. Check
        if len(sys.argv) == 3:
            if argv[i] == '-i':
                i_stock_list.append([argv[i+1]])

    # Loop through each stock csv file
    for i in range(len(i_stock_list)):
        i_stock = (i_stock_list[i].split('/')[-1]).split('.csv')[0]
        simlog.info("==================================================================================")
        simlog.info("Starting to process stock: " + str(i_stock))

        df = pd.read_csv(i_stock_list[i])

        # Step-1 Get data from each csv file and create a dataFrame.
        # Then pass on that dataFrame for stock prediction processing using AI models
        i_stock_object = STOCK_PREDICTION(simlog, i_stock, df)

        # Based on the suggestion from AI models, either BUY/SELL/No Nothing
        if not i_stock_object.action == stock_constants.STOCK_LEAVE:
            ALPACA(simlog, i_stock, i_stock_object.action)

        simlog.info("Pause for 1 second")
        time.sleep(1)
        simlog.info("==================================================================================")
    return 0

if __name__ == "__main__":
    main(sys.argv[1:])
