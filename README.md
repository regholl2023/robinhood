# robinhood
Tracks the stock prices and sends an alert of when to buy/sell stocks

# INFORMATION
There are several scripts that serves several different purposes

1) Get_Data.py: Is a python script that pulls the stocks data into the log
                folder (currently pulls data for 12 months)
                Example: python scripts/Get_Data.py --top_100
                         python scripts/Get_Data.py --all
                         python scripts/Get_Data.py --big_list

2) stock_analysis.py: Is also a python script that analyses the stock data
                      within the log folder.
                      -> Provides description/added details about the stocks
                      -> It makes recommendations on which stocks to buy/sell
                      -> Stocks that are recommended to buy/sell have added details
                         such as historic low/high price points, price slopes,
                         percentage difference from highest/lowest point and
                         averages.
