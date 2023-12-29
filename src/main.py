from daily import *
from hourly import *

from datetime import datetime

import MetaTrader5 as mt5
import pandas as pd
from pymongo import MongoClient

# tickers_list = open('resources/tickers.txt', 'r')
# tickers_list = tickers_list.readlines()
#
# count = 0
# for line in tickers_list:
#     count += 1
#     print("Line{}: {}".format(count, line.strip()))

tickers_list = ['PETR4', 'GGPS3']

run_daily(tickers_list)
run_hourly(tickers_list)

