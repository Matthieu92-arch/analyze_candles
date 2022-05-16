from telegram import telegram_bot_sendtext


def check_sfp_bullish(df_unique, df_check_far, df_check_close, market, minutes):
    idmax = df_check_far['low'].idxmin()


    if df_check_close['low'].min() < df_unique['low']:
        return

    if df_unique['low'] < df_check_far.loc[idmax]['low'] and \
            df_unique['close'] > df_check_far.loc[idmax]['close']:
        text = f'{market}  Bullish : {df_unique["startTime"]}'
        print(text)
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
        telegram_bot_sendtext(text, minutes)

    return


def check_sfp(market, df_candles, i, minutes):
    df_unique = df_candles.loc[i]
    df_check_far = df_candles.loc[i+25:i+151]
    df_check_close = df_candles.loc[i+1:i+25]

    check_sfp_bullish(df_unique, df_check_far, df_check_close, market, minutes)
    check_sfp_bearish(df_unique, df_check_far, df_check_close, market, minutes)

    return