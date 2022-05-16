import pandas as pd

from ftx.rest.client import FtxClient
from process import check_sfp

api_key = "Dl3Px24FKRjEs18ObF06uwB9GGpss9-q-IMyofzO"
api_secret = "LUqdaDI9U9kUlFXFq1G9iYFcVnCfPP1PmkQaxUH1"


# client = FtxClient(api_key, api_secret)
client = FtxClient(api_key, api_secret, 'trading')

markets = ['BTC-PERP', 'FTM-PERP', 'ATOM-PERP', 'SOL-PERP', 'LTC-PERP']
seconds_time = 1


def get_candles(market, minutes):
    return client.get_historical_prices(market, (minutes * 60))


def loop_candles(df_candles, market):
    for i in range(1, 1300):
        check_sfp(market, df_candles, i)


def launch_surveillance():
    for market in markets:
        df_candles = get_candles(market, seconds_time)
        df_candles = pd.DataFrame.from_records(df_candles)
        df_candles = df_candles[::-1].reset_index()
        print("Data obtained.")
        loop_candles(df_candles, market)


launch_surveillance()