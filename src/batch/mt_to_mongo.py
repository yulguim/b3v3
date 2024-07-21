from datetime import datetime
from pathlib import Path

from pymongo import MongoClient

from daily import *
from hourly import *

client = MongoClient("mongodb://192.168.31.188:27017/")

db = client.get_database('b3')

path = Path(__file__).parent / '../resources/tickers.txt'

tickers_list = open(path, 'r')
tickers_list = list(map(lambda x: x.strip(), tickers_list.readlines()))

start = datetime(2022, 1, 1)
end = datetime.now()

run_daily(tickers_list, start, end, db)
run_hourly(tickers_list, start, end, db)
