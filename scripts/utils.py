#!/usr/bin/python

import sys
import logging
import time
import string
import datetime
import random
import subprocess
from os import path
import csv


def read_CSV(i_file):
    i_data = []
    with open(i_file, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            i_data.append(row)
    return i_data
