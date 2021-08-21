#!/usr/bin/python


##############################################################################
#
# This file is used to generate blog from the recommendations.txt file
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
import sim_logging
import blog
from datetime import date
from datetime import datetime

def usage():
    print("Usage: Please provide the directory where recommendations.txt file is stored."
          "Defaults to the blog folder within the current directory")
    print("Example: python scripts/generate_blog.py")
    print("Example: python scripts/generate_blog.py --<location>")

def main(argv):

    if len(argv) > 1:
        print("Please provide only one directory")
        raise Exception
    elif len(argv) == 1:
        i_log_directory = argv[0]
    else:
        i_base_directory = os.path.abspath(os.path.dirname(sys.argv[0])).split('robinhood')[0]
        i_blog_directory = i_base_directory + "robinhood" + "/" + "blog" + "/"

    # Check if the recommendations file exist in the directory specified.
    # If not, exit the program
    if not os.path.exists(i_blog_directory + "recommendations.txt"):
        return

    simlog = sim_logging.SIMLOG(log_dir=i_blog_directory)
    # Delete existing log files if they exists
    if os.path.exists(i_blog_directory + "log.txt"):
        os.remove(i_blog_directory + "log.txt")

    # Step-1: Start reading the recommendations.txt file and extract key details about
    # the relevant stock
    i = 0
    i_stock_list = []
    i_file = open(i_blog_directory + "recommendations.txt", 'r')
    i_lines = i_file.readlines()
    while True:
        line = i_lines[i]
        if i_lines[i].__contains__('BUY:'):
            i_stock_object = blog.stock((i_lines[i + 1].split('=')[-1]).strip())
            i_stock_object.longName = (i_lines[i + 2].split('=')[-1]).strip()
            i_stock_object.sector = (i_lines[i + 3].split('=')[-1]).strip()
            i_stock_object.industry = (i_lines[i + 4].split('=')[-1]).strip()
            i_stock_object.slope = (i_lines[i + 5].split('=')[-1]).strip()
            i_stock_object.regularMarketPrice = (i_lines[i + 6].split('=')[-1]).strip()
            i_stock_object.lowest_stock_value = (i_lines[i + 7].split('=')[-1]).strip()
            i_stock_object.highest_stock_value = (i_lines[i + 8].split('=')[-1]).strip()
            i_stock_object.weighted_average = (i_lines[i + 9].split('=')[-1]).strip()
            i_stock_object.get_projections()
            i_stock_list.append(i_stock_object)
            i += 9
        else:
            # Jump out of the loop if you have reached the end of the line
            i += 1
            if i >= len(i_lines):
                del line, i_lines, i_stock_object, i
                break

    ######################################################################
    ######################################################################
    ######################################################################
    # Step-2: Create a blog now
    i_blog_file = i_blog_directory + "blog"

    # Remove any existing blog file
    if os.path.exists(i_blog_file):
        os.remove(i_blog_file)

    # Open file for writing
    blog_object = open(i_blog_file, 'a+')

    # Add header to the blog
    l_header = blog.get_header()
    blog_object.write(l_header + "\n")
    blog_object.write('Author: Saqib Khan' + "\n")
    blog_object.write('Published on ' + str(date.today().strftime("%B %d, %Y")) + " at " +
                      datetime.now().strftime("%H:%M:%S") + "\n")
    blog_object.write("\n\n\n")

    # Start adding stocks to the blog
    for i in range(len(i_stock_list)):
        blog_object.write(i_stock_list[i].longName + " (" + i_stock_list[i].shortName + ")" + ":\n")
        blog_object.write(i_stock_list[i].longBusinessSummary + "\n\n")

        # Get details about the stock
        l_details = blog.get_stock_performance_data(i_stock_list[i])
        blog_object.write(l_details + "\n\n")
        blog_object.write("\n\n")
    # Close the blog file
    blog_object.close()






if __name__ == "__main__":
    main(sys.argv[1:])
