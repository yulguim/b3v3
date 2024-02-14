from daily import *
from hourly import *

from datetime import datetime

import MetaTrader5 as mt5
import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://192.168.31.188:27017/")

# client.drop_database('b3')

tickers_list = open('resources/tickers.txt', 'r')
tickers_list = list(map(lambda x: x.strip(), tickers_list.readlines()))

start = datetime(2022, 1, 1)
end = datetime.now()

run_daily(tickers_list, start, end)
run_hourly(tickers_list)

tickers_list = open('resources/win.txt', 'r')
tickers_list = list(map(lambda x: x.strip(), tickers_list.readlines()))

run_daily(tickers_list, start, end)
run_hourly(tickers_list)