#!/usr/bin/python

import time
import sim_logging
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import REST, TimeFrame
import yfinance as yf
import stock_constants

class ALPACA:
    def __init__(self, i_keys, i_simlog, i_stock, i_action):
        self.simlog = i_simlog
        self.api = tradeapi.REST(i_keys.key[-1].strip(), i_keys.secretKey[-1].strip(), base_url=i_keys.url[-1].strip())
        #self.api = tradeapi.REST('PKCSBUUOKJN32C5LN716', 'aR9GddDWEcfgRHXUPOUtP6X7YI46JNOJsDUaFUBl',
        #                          base_url='https://paper-api.alpaca.markets')
        self.account = self.api.get_account()
        self.stock_name = i_stock
        self.action = i_action
        self.clear_unprocessed_orders()
        self.list_positions = self.api.list_positions()
        self.process_data()
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
            if i_current_invested < 5:
                i_qty = float(2/float(i_current_price))

                # Round down stock quantity if > 1
                if i_qty > 1:
                    i_qty = int(i_qty)
                    self.simlog.info("Quantity of shares to buy: " + str(i_qty))
                    self.simlog.info("We are going to BUY " + str(self.stock_name))
                    l_result = self.api.submit_order(symbol=self.stock_name, qty=i_qty,
                                        side='buy', type='market', time_in_force='gtc')
                else:
                    try:
                        l_result = self.api.submit_order(symbol=self.stock_name, qty=i_qty,
                                    side='buy', type='market', time_in_force='day')
                    except Exception as e:
                        print(e)
                        return

        # Sell all current quantity of this stock
        elif self.action == stock_constants.STOCK_SELL:
            if i_current_quantity > 0:

                # It is possible that we are looking at a loss on this trade.
                # Thus hold onto the stock for a while and don't sell
                for i in range(len(self.list_positions)):
                    if self.list_positions[i].symbol == str(self.stock_name):
                        #unrealized_plpc needs to be multiplied by 100 to get the percentage
                        if float(self.list_positions[i].unrealized_plpc) >= 0.02:
                            self.simlog.info("We are going to SELL " + str(self.stock_name))
                            l_result = self.api.submit_order(symbol=self.stock_name, qty=i_current_quantity,
                                                 side='sell', type='market', time_in_force='day')
                            self.simlog.warning("realized_plpc = " + str(self.list_positions[i].unrealized_plpc))
                            return
                        else:
                            self.simlog.warning("It was recommended to sell " + str(self.stock_name))
                            self.simlog.warning("We are not selling because there is a profit/loss of $" + str(self.list_positions[i].unrealized_pl))
                            self.simlog.warning("unrealized_plpc = " + str(self.list_positions[i].unrealized_plpc))
                            return
        else:
            print("The following action is undefined: " + str(self.action))
            raise Exception

# Create an API object
#api = tradeapi.REST('PKCSBUUOKJN32C5LN716', 'aR9GddDWEcfgRHXUPOUtP6X7YI46JNOJsDUaFUBl',
#                    base_url='https://paper-api.alpaca.markets')
