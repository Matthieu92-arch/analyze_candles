from telegram import telegram_bot_sendtext
import hashlib


def alert_exist_in_saved(hash_alerts, market, startTime):
    hash_result = f'{market}{startTime}'
    hash_object = hashlib.md5(hash_result.encode())

    if not hash_alerts or len(hash_alerts) == 0:
        return False
    if hash_object.hexdigest() in hash_alerts:
        return True
    return False


def check_sfp_bullish(df_unique, df_check_far, df_check_close, market, minutes, hash_alerts):
    idmax = df_check_far['low'].idxmin()

    if df_check_close['low'].min() < df_unique['low'] or alert_exist_in_saved(hash_alerts, market, df_unique["startTime"]):
        return hash_alerts


    if df_unique['low'] < df_check_far.loc[idmax]['low'] and \
            df_unique['close'] > df_check_far.loc[idmax]['close']:
        hash_result = f'{market}{df_unique["startTime"]}'
        hash_object = hashlib.md5(hash_result.encode())
        hash_alerts.append(hash_object.hexdigest())
        text = f'{market}  Bullish : {df_unique["startTime"]}'

        print(f'{text}  -> {hash_object.hexdigest()}')
        telegram_bot_sendtext(text, minutes)

    return hash_alerts


def check_sfp_bearish(df_unique, df_check_far, df_check_close, market, minutes, hash_alerts):
    idmax = df_check_far['high'].idxmax()

    if df_check_close['high'].max() > df_unique['high'] or alert_exist_in_saved(hash_alerts, market, df_unique["startTime"]):
        return hash_alerts

    if df_unique['high'] > df_check_far.loc[idmax]['high'] and \
            df_unique['close'] < df_check_far.loc[idmax]['close']:
        hash_result = f'{market}{df_unique["startTime"]}'
        hash_object = hashlib.md5(hash_result.encode())
        hash_alerts.append(hash_object.hexdigest())
        text = f'{market}  Bearish : {df_unique["startTime"]}'

        print(f'{text}  -> {hash_object.hexdigest()}')
        telegram_bot_sendtext(text, minutes)

    return hash_alerts


def check_sfp(market, df_candles, i, minutes, far_candle, hash_alerts):
    df_unique = df_candles.loc[i]
    df_check_far = df_candles.loc[i+25:i+far_candle]
    df_check_close = df_candles.loc[i+1:i+25]

    hash_alerts = check_sfp_bullish(df_unique, df_check_far, df_check_close, market, minutes, hash_alerts)
    hash_alerts = check_sfp_bearish(df_unique, df_check_far, df_check_close, market, minutes, hash_alerts)

    return hash_alerts