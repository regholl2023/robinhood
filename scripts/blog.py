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
import sim_logging
from scipy.stats import linregress

Header_list = ["Top stocks to invest in right now",
               "Hottest stocks right now",
               "Best stocks to buy now",
               "Top Growth Stocks to invest in",
               "Best stocks to buy for the rest of the year",
               "Top stocks for 2021",
               "Stocks with highest potential",
               "Which stocks to invest if you have $1000 right now",
               "Stocks with highest potential for growth"]


def get_header():
    return random.choice(Header_list)


def get_stock_performance_data(i_stock_object):
    l_option1 = "Over the last 12 months, the stock " + i_stock_object.shortName + \
                " has reached a maximum market price of $" + i_stock_object.highest_stock_value + \
                " and is now trading at a discounted price of $" + str(i_stock_object.regularMarketPrice) + \
                ". The stock is currently very close to the 12 month lowest price point of $" + \
                str(i_stock_object.lowest_stock_value) + ", which is why this is the best time to get in. " + \
                "Analysts states that " + i_stock_object.shortName + " is projected to reach $" + \
                str(i_stock_object.projected_price_12_months) + " over the next 12 months."

    l_option2 = "Over the last 12 months, the stock " + i_stock_object.shortName + \
                " has reached a maximum market price of $" + i_stock_object.highest_stock_value + \
                " and is now trading at a discounted price of $" + str(i_stock_object.regularMarketPrice) + \
                ". The stock is very close to the 12 month lowest price point of $" + \
                str(i_stock_object.lowest_stock_value) + ", which is why this is the best time to get in. " + \
                i_stock_object.shortName + " is projected to reach $" + \
                str(i_stock_object.projected_price_6_months) + " over the next 6 months."

    l_option3 = "Over the last 12 months, the stock " + i_stock_object.shortName + \
                " has reached a maximum market price of $" + i_stock_object.highest_stock_value + \
                " and is now trading at a price of $" + str(i_stock_object.regularMarketPrice) + \
                ". The stock is currently very close to the 12 month lowest price point of $" + \
                str(i_stock_object.lowest_stock_value) + ", which is why this is the best time to get in. " + \
                i_stock_object.shortName + " is projected to reach $" + \
                str(i_stock_object.projected_price_24_months) + " over the next 24 months."

    l_option4 = "Over the last 12 months, the stock " + i_stock_object.shortName + \
                " has reached a maximum market price of $" + i_stock_object.highest_stock_value + \
                " and is now trading at a discounted price of $" + str(i_stock_object.regularMarketPrice) + \
                ". The stock is currently very close to the 12 month lowest price point of $" + \
                str(i_stock_object.lowest_stock_value) + ", which is why this is the best time to get in."

    l_option5 = "Over the past year, the stock " + i_stock_object.shortName + \
                " has peaked at a maximum market price of $" + i_stock_object.highest_stock_value + \
                " and is currently trading at a price of $" + str(i_stock_object.regularMarketPrice) + ". " + \
                i_stock_object.shortName + " is projected to reach $" + \
                str(i_stock_object.projected_price_12_months) + " by next year."

    l_option6 = "Over the past year the stock " + i_stock_object.shortName + \
                " has peaked at a maximum market price of $" + i_stock_object.highest_stock_value + \
                " and is trading at a price of $" + str(i_stock_object.regularMarketPrice) + ". " + \
                i_stock_object.shortName + " is projected to reach $" + \
                str(i_stock_object.projected_price_24_months) + " over the next 24 months."

    l_option7 = "Over the past year the stock " + i_stock_object.shortName + \
                " has peaked at a maximum market price of $" + i_stock_object.highest_stock_value + \
                " and is currently trading at a price of $" + str(i_stock_object.regularMarketPrice) + ". " + \
                i_stock_object.shortName + " is projected to reach $" + \
                str(i_stock_object.projected_price_6_months) + " over the next 6 months."

    l_option8 = "The stock " + i_stock_object.shortName + " is currently traded at $" + \
                str(i_stock_object.regularMarketPrice) + " and is expected to reach $" + \
                str(i_stock_object.projected_price_6_months) + " over the next 6 months. The 12 month maximum " \
                "value for " + i_stock_object.shortName + " is $" + i_stock_object.highest_stock_value + \
                " while the 12 month lowest selling price was $" + i_stock_object.lowest_stock_value + \
                ". The current selling price is very close to the lowest selling point, which makes this stock a" \
                " must buy."

    l_option9 = "The stock " + i_stock_object.shortName + " is currently traded at $" + \
                str(i_stock_object.regularMarketPrice) + " and is expected to reach $" + \
                str(i_stock_object.projected_price_12_months) + " over the next 12 months. The 12 month maximum " \
                "value for " + i_stock_object.shortName + " is $" + i_stock_object.highest_stock_value + \
                " while the 12 month lowest selling price was $" + i_stock_object.lowest_stock_value + \
                ". The current selling price is very close to the lowest selling point, which makes this stock a" \
                " must buy."

    l_option10 = "The stock " + i_stock_object.shortName + " is currently traded at $" + \
                 str(i_stock_object.regularMarketPrice) + " and is expected to reach $" + \
                 str(i_stock_object.projected_price_24_months) + " over the next 24 months. The 12 month maximum " \
                 "value for " + i_stock_object.shortName + " is $" + i_stock_object.highest_stock_value + \
                 " while the 12 month lowest selling price was $" + i_stock_object.lowest_stock_value + \
                 ". The current selling price is very close to the lowest selling point, which makes this stock a" \
                 " must buy."

    l_option11 = "The stock " + i_stock_object.shortName + " is currently traded at $" + \
                 str(i_stock_object.regularMarketPrice) + " and is expected to reach $" + \
                 str(i_stock_object.projected_price_12_months) + " by next year. The 12 month maximum " \
                 "value for " + i_stock_object.shortName + " is $" + i_stock_object.highest_stock_value + \
                 " while the 12 month lowest selling price was $" + i_stock_object.lowest_stock_value + \
                 ". The current selling price is very close to the lowest selling point, which makes this stock a" \
                 " must buy."

    l_options = [l_option1, l_option2, l_option3, l_option4, l_option5, l_option6, l_option7, l_option8, l_option9,
                 l_option10, l_option11]
    return random.choice(l_options)


class stock:
    def __init__(self, i_name):
        self.shortName = i_name
        self.longName = None
        self.sector = None
        self.industry = None
        self.slope = None
        self.regularMarketPrice = None
        self.lowest_stock_value = None
        self.highest_stock_value = None
        self.weighted_average = None

        self.ticker_object = yf.Ticker(self.shortName)
        self.longBusinessSummary = None
        self.divident = None
        self.headquarters_location = None

        self.projected_price_24_months = None
        self.projected_price_12_months = None
        self.projected_price_6_months = None

        self.get_extra_info()

    def get_extra_info(self):
        # This is the long description of what the business does
        self.longBusinessSummary = self.ticker_object.info['longBusinessSummary']

        l_city = self.ticker_object.info['city']
        l_country = self.ticker_object.info['country']
        # It is possible that the state info doesn't exist. Therefore use a try/except to catch such errors
        try:
            l_state = self.ticker_object.info['state']
            self.headquarters_location = l_city + ", " + l_state + ", " + l_country
        except:
            self.headquarters_location = l_city + ", " + l_country

    def get_projections(self):
        self.regularMarketPrice = str(round(float(self.regularMarketPrice), 2))
        self.lowest_stock_value = str(round(float(self.lowest_stock_value), 2))
        self.highest_stock_value = str(round(float(self.highest_stock_value), 2))
        self.weighted_average = str(round(float(self.weighted_average), 2))

        self.projected_price_6_months = str(round(float(self.regularMarketPrice) + (float(self.slope) * 6), 2))
        self.projected_price_12_months = str(round(float(self.regularMarketPrice) + (float(self.slope) * 12), 2))
        self.projected_price_24_months = str(round(float(self.regularMarketPrice) + (float(self.slope) * 24), 2))
