from telegram import telegram_bot_sendtext
import hashlib


def alert_exist_in_saved(df_saved, df_unique, market):
    if df_saved.empty:
        return False

    df_sv = df_saved.loc[df_saved['pair'] == market]
    return True if df_unique['startTime'] in df_sv.startTime.to_list() else False
    # df_unique['startTime'] in df_sv.startTime.to_list() ? return True else False
    # df_sv = df_saved.loc[(df_saved['startTime'] == df_unique['startTime']) & (df_saved['volume'] == df_unique['volume'])]
    # if not df_sv.empty:
    #     return True
    return False

def check_sfp_bullish(df_unique, df_check_far, df_check_close, market, minutes):
    idmax = df_check_far['low'].idxmin()


    if df_check_close['low'].min() < df_unique['low']:
        return

    if df_unique['low'] < df_check_far.loc[idmax]['low'] and \
            df_unique['close'] > df_check_far.loc[idmax]['close']:
        text = f'{market}  Bullish : {df_unique["startTime"]}'
        print(text)
        hash_object = hashlib.md5(text.encode())
        print(hash_object.hexdigest())

        df_unique['pair'] = [market]
        telegram_bot_sendtext(text, minutes)

    return


def check_sfp_bearish(df_unique, df_check_far, df_check_close, market, minutes):
    idmax = df_check_far['high'].idxmax()

    if df_check_close['high'].max() > df_unique['high']:
        return

    if df_unique['high'] > df_check_far.loc[idmax]['high'] and \
            df_unique['close'] < df_check_far.loc[idmax]['close']:
        text = f'{market}  Bearish : {df_unique["startTime"]}'
        print(text)
        hash_object = hashlib.md5(text.encode())
        print(hash_object.hexdigest())

        df_unique['pair'] = market
        telegram_bot_sendtext(text, minutes)

    return


def check_sfp(market, df_candles, i, minutes, far_candle):
    df_unique = df_candles.loc[i]
    df_check_far = df_candles.loc[i+25:i+far_candle]
    df_check_close = df_candles.loc[i+1:i+25]

    check_sfp_bullish(df_unique, df_check_far, df_check_close, market, minutes)
    check_sfp_bearish(df_unique, df_check_far, df_check_close, market, minutes)

    return