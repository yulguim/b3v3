from datetime import datetime

import MetaTrader5 as mt5
import pandas as pd
from pymongo.database import Database


def run_daily(tickers: list, start: datetime, end: datetime, db: Database):
    print(tickers)

    collection = db.get_collection('stockHistory')

    mt5.initialize()

    for ticker in tickers:
        if collection.count_documents({'ticker': ticker}) > 0:
            continue

        print(ticker)

        data = mt5.copy_rates_range(
            ticker,
            mt5.TIMEFRAME_D1,
            start,
            end,
        )

        data = pd.DataFrame(data)

        if 'time' not in data.columns:
            print('{} no time', ticker)
            continue

        # Converter data
        data['time'] = pd.to_datetime(data['time'], unit='s')

        previous_close = None
        previous_date = None

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

            if previous_close is not None:
                top = ticker_history['open'] - previous_close
                bottom = abs(previous_close)
                percentage_change_from_previous_close_and_open = round((top / bottom) * 100, 4)
                document['percentageChangeFromPreviousCloseAndOpen'] = percentage_change_from_previous_close_and_open

            previous_close = ticker_history['close']
            previous_date = ticker_history['time']

            collection.insert_one(document)

    mt5.shutdown()

