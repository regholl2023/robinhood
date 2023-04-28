#!/usr/bin/python

import sim_logging
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import REST, TimeFrame
import stock_constants

class ALPACA:
    def __init__(self, i_simlog, i_stock, i_action):
        self.simlog = i_simlog
        self.api = tradeapi.REST('PKCSBUUOKJN32C5LN716', 'aR9GddDWEcfgRHXUPOUtP6X7YI46JNOJsDUaFUBl',
                                  base_url='https://paper-api.alpaca.markets')
        self.account = self.api.get_account()
        self.stock_name = i_stock
        self.action = i_action
        self.list_positions = self.api.list_positions()
        self.process_data()


    def process_data(self):
        i_current_price = float(self.api.get_bars(self.stock_name, TimeFrame.Hour, limit=1)[0].c)
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
                i_qty = float(10/float(self.list_positions[i].current_price))
                l_result = self.api.submit_order(symbol=self.stock_name, qty=i_qty,
                                    side='buy', type='market', time_in_force='day')

        # Sell all current quantity of this stock
        elif self.action == stock_constants.STOCK_SELL:
            if i_current_quantity > 0:
                l_result = self.api.submit_order(symbol=self.stock_name, qty=i_current_quantity,
                                     side='sell', type='market', time_in_force='day')
        else:
            print("The following action is undefined: " + str(self.action))
            raise Exception

# Create an API object
#api = tradeapi.REST('PKCSBUUOKJN32C5LN716', 'aR9GddDWEcfgRHXUPOUtP6X7YI46JNOJsDUaFUBl',
#                    base_url='https://paper-api.alpaca.markets')