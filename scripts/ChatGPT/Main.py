#!/usr/bin/python


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


# ---------Set sys.path for MAIN execution---------------------------------------
full_path = os.path.abspath(os.path.dirname(sys.argv[0])).split('robinhood')[0]
full_path += "robinhood"
sys.path.append(full_path)
# Walk path and append to sys.path
for root, dirs, files in os.walk(full_path):
    for dir in dirs:
        sys.path.append(os.path.join(root, dir))



def main(argv):
    x = 1


if __name__ == "__main__":
    main(sys.argv[1:])
