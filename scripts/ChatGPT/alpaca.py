#!/usr/bin/python

import alpaca_trade_api as tradeapi

# Create an API object
api = tradeapi.REST('PKCSBUUOKJN32C5LN716', 'aR9GddDWEcfgRHXUPOUtP6X7YI46JNOJsDUaFUBl',
                    base_url='https://paper-api.alpaca.markets')

# Define the stock you want to retrieve data for
symbol = 'AAPL'

account = api.get_account()
print(account)

# Place an order
#api.submit_order(
#    symbol='AAPL',
#    qty=1,
#    side='buy',
#    type='market',
#    time_in_force='gtc'
#)