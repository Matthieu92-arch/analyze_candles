import requests



bot_token = "1431812434:AAEY4B1W8l73Cxfg67Tsebazn2IReGRzrAA"
bot_chatID = "827659849"


def telegram_bot_sendtext(text, minutes):
    message = f"--------Sfp {minutes} min--------\n"
    message += text
    message += f"\n-----------------------\n"

    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + message

    response = requests.get(send_text)

    return response.json()

