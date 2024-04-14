from datetime import datetime

from pymongo import MongoClient
import MetaTrader5 as mt5
import pandas as pd


def run_hourly(tickers: list, start: datetime, end: datetime):
    client = MongoClient("mongodb://192.168.31.188:27017/")

    db = client.get_database('b3')

    collection = db.get_collection('stockHistory')

    mt5.initialize()

    for ticker in tickers:
        data = mt5.copy_rates_range(
            ticker,
            mt5.TIMEFRAME_H1,
            start,
            end,
        )

        data = pd.DataFrame(data)

        if 'time' not in data.columns:
            print('{} no time', ticker)
            continue

        print('{} time', ticker)

        data['time'] = pd.to_datetime(data['time'], unit='s')

        list = {}

        for index, ticker_history in data.iterrows():
            day_to_update = ticker_history['time'].strftime('%d-%m-%Y')
            key = ticker + '_' + day_to_update
            if list.get(key) is None:
                list[key] = []

            document = {
                'date': ticker_history['time'],
                'open': ticker_history['open'],
                'close': ticker_history['close']
            }

            list[key].append(document)

        for key, value in list.items():
            result = collection.update_one({'key': key}, {'$set': {'hourly': value}})
            print("match:{}, modified:{}".format(result.matched_count, result.modified_count))

    mt5.shutdown()

