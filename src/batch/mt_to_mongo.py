from pathlib import Path

from pymongo import MongoClient

import config
from daily import *
from hourly import *

client = MongoClient(config.MONGODB_URL)

db = client.get_database(config.MONGODB_DATABASE)

path = Path(__file__).parent / '../resources/tickers.txt'

tickers_list = open(path, 'r')
tickers_list = list(map(lambda x: x.strip(), tickers_list.readlines()))

start = datetime(config.START_YEAR, 1, 1)
end = datetime.now()

run_daily(tickers_list, start, end, db)
run_hourly(tickers_list, start, end, db)
