from datetime import datetime

import MetaTrader5 as mt5
import pandas as pd
from pymongo.database import Database


def run_hourly(tickers: list, start: datetime, end: datetime, db: Database):
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
                'close': ticker_history['close'],
                'high': ticker_history['high'],
                'low': ticker_history['low'],
                'volume': ticker_history['real_volume'],
            }

            list[key].append(document)

        for key, value in list.items():
            result = collection.update_one({'key': key}, {'$set': {'hourly': value}})
            print("ticker:{}, match:{}, modified:{}".format(ticker, result.matched_count, result.modified_count))

    mt5.shutdown()

