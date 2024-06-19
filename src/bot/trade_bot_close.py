import MetaTrader5 as mt5

mt5.initialize()

orders_total = mt5.orders_total()
print('total orders: {}'.format(orders_total))

orders = mt5.orders_get()

for order in orders:
    print(order)

    result_object = mt5.order_send({
        "order": order.ticket,
        "action": mt5.TRADE_ACTION_REMOVE
    })

    if result_object is None:
        print(mt5.last_error())
    else:
        print(result_object)

mt5.shutdown()
