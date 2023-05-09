#!/usr/bin/python

import time
import sim_logging
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import REST, TimeFrame
import yfinance as yf
import stock_constants

class ALPACA:
    def __init__(self, i_simlog, i_stock, i_action):
        self.simlog = i_simlog
        self.api = tradeapi.REST('PKCSBUUOKJN32C5LN716', 'aR9GddDWEcfgRHXUPOUtP6X7YI46JNOJsDUaFUBl',
                                  base_url='https://paper-api.alpaca.markets')
        self.account = self.api.get_account()
        self.stock_name = i_stock
        self.action = i_action
        self.clear_unprocessed_orders()
        self.list_positions = self.api.list_positions()
        self.process_data()

        self.simlog.info("Sleeping for 1 sec")
        time.sleep(1)
        self.clear_unprocessed_orders()

    def clear_unprocessed_orders(self):
        open_orders = self.api.list_orders(status='open')
        for order in open_orders:
            if order.filled_qty == '0':
                self.api.cancel_order(order.id)

    def process_data(self):
        # It is possible that there was an issue with pulling stock data from alpaca.
        # So retry with yahoo finance
        try:
            try:
                i_current_price = float(self.api.get_bars(self.stock_name, TimeFrame.Hour, limit=1)[0].c)
            except:
                tickerData = yf.Ticker(self.stock_name); 
                i_current_price = tickerData.history(period='1d')['Close'][0]
        except IndexError as e:
            self.simlog.error("Failed to get current stock price for " + str(self.stock_name))
            self.simlog.error(str(e))
            return

        i_current_quantity = int(0) #Number of stocks for this particular symbol
        i_current_invested = float(0) #Calculated by multiplying quantity with market_value

        for i in range(len(self.list_positions)):
            if self.stock_name == self.list_positions[i].symbol:
                i_current_quantity = float(self.list_positions[i].qty)
                i_current_invested = float(self.list_positions[i].qty) * float(self.list_positions[i].current_price)

        # No Action Needed at this time for the particular stock
        if self.action == stock_constants.STOCK_LEAVE:
            return

        elif self.action == stock_constants.STOCK_BUY:
            if i_current_invested < 1000:
                i_qty = float(100/float(i_current_price))

                # There are some stocks that don't trade fractional  shares.
                # These are usually stocks that are below $1. Therefore round
                # down the quantity
                if i_current_price < 1:
                    i_qty = int(i_qty)

                self.simlog.info("We are going to BUY " + str(self.stock_name))
                l_result = self.api.submit_order(symbol=self.stock_name, qty=i_qty,
                                    side='buy', type='market', time_in_force='day')

        # Sell all current quantity of this stock
        elif self.action == stock_constants.STOCK_SELL:
            if i_current_quantity > 0:
                self.simlog.info("We are going to SELL " + str(self.stock_name))
                l_result = self.api.submit_order(symbol=self.stock_name, qty=i_current_quantity,
                                     side='sell', type='market', time_in_force='day')
        else:
            print("The following action is undefined: " + str(self.action))
            raise Exception

# Create an API object
#api = tradeapi.REST('PKCSBUUOKJN32C5LN716', 'aR9GddDWEcfgRHXUPOUtP6X7YI46JNOJsDUaFUBl',
#                    base_url='https://paper-api.alpaca.markets')
