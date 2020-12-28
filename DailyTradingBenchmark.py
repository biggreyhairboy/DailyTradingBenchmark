"""
calculate daily average true range of latest 20 days(atr20)
outpu csv
"""
import json
import string
from WindPy import *
import pandas as pd



def get_atr20(active_contract, active_date, atr_range=20):
    search_contracts = ",".join(active_contract)
    other_parameters ="ATR_N=" + str(atr_range) + ";ATR_IO=1;TradingCalendar=SHFE"
    data = w.wsd(search_contracts, "ATR", "ED0TD", active_date, other_parameters)
    print((data.Data)[0])
    return (data.Data)[0]

def get_contract_mutiplier(active_contract, active_date):
    search_contracts = ",".join(active_contract)
    data = w.wsd(search_contracts, "contractmultiplier", "ED0TD", active_date, "TradingCalendar=SHFE")
    return (data.Data)[0]
    print((data.Data)[0])


def fmt_active_contracts():
    all_contracts = []
    for exchange, sc in config["active_contracts"].items():
        for symbol, contract in sc.items():
            acontract = contract + "." + get_exchange(contract)
            all_contracts.append(acontract)
    return all_contracts


def get_exchange(contract):
    symbol = contract.rstrip(string.digits)
    for exchange, symbols in config["exchanges"].items():
        if symbol in symbols:
            return exchange


def format_wind_date():
    active_date = config["trading_date"]
    return active_date
    pass


if __name__ == "__main__":
    # execute only if run as a script
    w.start()
    with open("DailyTradingBenchmark.json") as f:
        config = json.load(f)
    trading_date = format_wind_date()
    active_contracts = fmt_active_contracts()
    atr20 = get_atr20(active_contracts, trading_date)
    multiplier = get_contract_mutiplier(active_contracts, trading_date)
    contracts_df = pd.DataFrame({"contracts": active_contracts, "atr20": atr20, "multiplier": multiplier})
    principal_vol = config["principal"] * 0.03
    contracts_df["max_vol"] = contracts_df.atr20 * contracts_df.multiplier
    contracts_df["tradable"] = contracts_df.max_vol.apply(
        lambda x: (True if x < principal_vol else False)
    )
    print(contracts_df.loc[contracts_df["tradable"] == True])
    # print(contracts_df)

