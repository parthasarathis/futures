import requests
import datetime


def send_msg(text):
    token = "5553248552:AAH8jBah0G3Do_W87HfDNnkB3dK7x-HpNU0"
    chat_id = "963108122"
    url_req = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}"
    results = requests.get(url_req)


# Get the current time
current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Send the current time to your Telegram bot
send_msg(current_time)
