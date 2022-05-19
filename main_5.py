from time import sleep

import pandas as pd


from ftx.rest.client import FtxClient
from process import check_sfp
from save_datas import read_list_from_file, write_list_to_file

pd.options.mode.chained_assignment = None

api_key = "Dl3Px24FKRjEs18ObF06uwB9GGpss9-q-IMyofzO"
api_secret = "LUqdaDI9U9kUlFXFq1G9iYFcVnCfPP1PmkQaxUH1"

client = FtxClient(api_key, api_secret, 'trading')

markets = ['BTC-PERP', 'ETH-PERP', 'FTM-PERP', 'ATOM-PERP', 'BNB-PERP',
           'LTC-PERP', 'DOT-PERP', 'ETH-PERP', 'MATIC-PERP']
# markets = ['BNB-PERP']
seconds_time = 5


def get_candles(market, minutes):
    return client.get_historical_prices(market, (minutes * 60))


def loop_candles(df_candles, market, min, far_candle, hash_alerts):
    print(market)
    for i in range(1, 7):
        hash_alerts = check_sfp(market, df_candles, i, min, far_candle, hash_alerts)
    return hash_alerts


def launch_surveillance():
    sleep(5)
    far_candle = 74
    file_name = 'output_5.txt'
    hash_alerts = read_list_from_file(file_name)

    for market in markets:
        df_candles = get_candles(market, seconds_time)
        df_candles = pd.DataFrame.from_records(df_candles)
        df_candles = df_candles[::-1].reset_index()
        print("Data obtained.")
        hash_alerts = loop_candles(df_candles, market, 5, far_candle, hash_alerts)

    write_list_to_file(file_name, hash_alerts)
    print("Done")

launch_surveillance()