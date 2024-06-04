def print_symbol_info(symbol_info):
    # display the terminal data 'as is'
    print(symbol_info)
    print("spread =", symbol_info.spread, "  digits =", symbol_info.digits)
    # display symbol properties as a list
    print("Show symbol_info._asdict():")
    symbol_info_dict = symbol_info._asdict()
    for prop in symbol_info_dict:
        print("  {}={}".format(prop, symbol_info_dict[prop]))

    print("\n\n\n\n\n -------- \n\n\n\n\n")
