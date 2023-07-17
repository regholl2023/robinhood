# robinhood
Tracks the stock prices and sends an alert of when to buy/sell stocks

# Required packages
For Ubuntu:

   sudo apt-get update
   
   sudo apt-get upgrade
   
   sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget pip python python3 libxml2-dev libxslt-dev python-dev libatlas-base-dev gfortran cmake
   
   sudo pip3 install numpy pandas yfinance plotly scipy tabulate sklearn xgboost keras tensorflow

# INFORMATION
There are several scripts that serves several different purposes

1) Get_Data.py: Is a python script that pulls the stocks data into the log
                folder (currently pulls data for 12 months)
                
                Example: python3 scripts/Get_Data.py --top_100
                
                         python3 scripts/Get_Data.py --all
                         
                         python3 scripts/Get_Data.py --big_list
                         
                         

2) stock_analysis.py: Is also a python script that analyses the stock data
                      within the log folder.
                      -> Provides description/added details about the stocks
                      -> It makes recommendations on which stocks to buy/sell
                      -> Stocks that are recommended to buy/sell have added details
                         such as historic low/high price points, price slopes,
                         percentage difference from highest/lowest point and
                         averages.
                         
                      Example: python3 scripts/stock_analysis.py

# Lessons Learned
1) When there is too much money in the system, useless stocks tends to go high up in value. Penny stock increases exponentially in value.
2) When the money supply shrinks, people sell more risky stocks and invest in more stable stocks. Google and Amazon goes up, while penny stocks go down.
