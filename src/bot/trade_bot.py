import os

import MetaTrader5 as mt5

from strategy_details import StrategyDetails

strategy_path = '../resources/strategies.txt'
strategy_path = os.path.join(os.path.dirname(__file__), strategy_path)

strategy_list = open(strategy_path, "r")
strategy_list = list(map(lambda x: x.strip(), strategy_list.readlines()))

mt5.initialize()

for line in strategy_list:
    if line.startswith("#"):
        print("Skipping line: {}".format(line))
        continue

    line = line.split(";")
    info = StrategyDetails(line[0], float(line[1]), int(line[2]))

    symbol_info = mt5.symbol_info(info.ticker)
    if symbol_info is None:
        continue

    last_close = symbol_info.session_close

    buy_price = round(last_close * ((100.0 - (info.percentage * - 1.0)) / 100), 2)

    comment = info.ticker + ': ' + str(info.percentage)

    print('ticker:{} percentage:{} quantity:{} last_close:{} buy_price:{}'
          .format(info.ticker, info.percentage, info.quantity, last_close, buy_price)
          )

    result_object = mt5.order_send(
        {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": info.ticker,
            "volume": float(info.quantity),
            "type": mt5.ORDER_TYPE_BUY_LIMIT,
            "price": buy_price,
            "magic": 100,
            "comment": comment,
            "type_time": mt5.ORDER_TIME_DAY,
            "type_filling": mt5.ORDER_FILLING_RETURN
        }
    )

    if result_object is None:
        print(mt5.last_error())
    else:
        print(result_object)


mt5.shutdown()
