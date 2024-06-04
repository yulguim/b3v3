import MetaTrader5 as mt5
import pandas as pd

from datetime import datetime

from src.bot.symbol_info_util import print_symbol_info
from src.models.strategy_details import StrategyDetails

strategy_list = open("../resources/strategies.txt", "r")
strategy_list = list(map(lambda x: x.strip(), strategy_list.readlines()))

mt5.initialize()

result_object = mt5.order_send(
    {
        "action": mt5.TRADE_ACTION_DEAL,    # ação imediata de transação
        "symbol": 'PETR4',
        "volume": 0.0001,
        "type": mt5.ORDER_TYPE_BUY,         # ordem de mercado para compra
        "price": 10.50,                     # preço ask
        "sl": None,          # não é necessário
        "tp": None,          # não é necessário
        "deviation": 0.1,
        "magic": 234000,
        "comment": "asimov python script open",
        "type_time": mt5.ORDER_TIME_GTC,            # A ordem permanecerá na fila até ser tirada
        "type_filling": mt5.ORDER_FILLING_RETURN,   # Ordem manual
    }
)

print(result_object)

result_dict = result_object._asdict()
for field in result_dict.keys():
    print(f"   {field}={result_dict[field]}")
    #se esta for uma estrutura de uma solicitação de negociação, também a exibiremos elemento a elemento
    if field == "request":
        traderequest_dict = result_dict[field]._asdict()
        for tradereq_filed in traderequest_dict:
            print(f"\ttraderequest: {tradereq_filed}={traderequest_dict[tradereq_filed]}")

for line in strategy_list:
    line = line.split(";")
    info = StrategyDetails(line[0], float(line[1]), int(line[2]))

    symbol_info = mt5.symbol_info(info.ticker)
    if symbol_info is None:
        continue

    # print_symbol_info(symbol_info)

    last_close = symbol_info.session_close

    buy_price = round(last_close * ((100.0 - (info.percentage * - 1.0)) / 100), 2)

    print('ticker:{} percentage:{} quantity:{} last_close:{} buy_price:{}'
          .format(info.ticker, info.percentage, info.quantity, last_close, buy_price)
          )

# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
