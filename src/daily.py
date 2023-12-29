from datetime import datetime

from pymongo import MongoClient
import MetaTrader5 as mt5
import pandas as pd


def run_daily(tickers: list):
    print(tickers)

    client = MongoClient("mongodb://192.168.31.188:27017/")

    db = client.get_database('b3')

    collection = db.get_collection('stockHistory')

    mt5.initialize()

    for ticker in tickers:
        print(ticker)

        data = mt5.copy_rates_range(
            ticker,
            mt5.TIMEFRAME_D1,
            datetime(2021, 12, 1),
            datetime(2023, 12, 31),
        )

        data = pd.DataFrame(data)

        print(data)

        data['time'] = pd.to_datetime(data['time'], unit='s')

        for index, ticker_history in data.iterrows():
            date_str = ticker_history['time'].strftime('%d-%m-%Y')

            document = {
                'ticker': ticker,
                'key': ticker + '_' + date_str,
                'date': ticker_history['time'],
                'open': ticker_history['open'],
                'close': ticker_history['close'],
                'high': ticker_history['high'],
                'low': ticker_history['low'],
                'volume': ticker_history['real_volume'],
                'dateStr': date_str,
                'previousClose': previous_close,
                'previousCloseDate': previous_date
            }

            print(document)

            collection.insert_one(document)

    mt5.shutdown()

