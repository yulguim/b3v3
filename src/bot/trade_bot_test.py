import MetaTrader5 as mt5

mt5.initialize()

result_object = mt5.order_send(
    {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": 'MGLU3F',
        "volume": 5.0,
        "type": mt5.ORDER_TYPE_BUY_LIMIT,
        "price": 7.50,
        "magic": 234000,
        "comment": "MGLU3F",
        "type_time": mt5.ORDER_TIME_DAY,
        "type_filling": mt5.ORDER_FILLING_RETURN
    }
)

if result_object is None:
    print(mt5.last_error())
else:
    print(result_object)

mt5.shutdown()
