import requests
from keys import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
print(requests.get(url).json())

def send_msg(text):
    token = TELEGRAM_TOKEN
    chat_id = TELEGRAM_CHAT_ID
    url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text
    results = requests.get(url_req)
    print(results.json())

send_msg("Hello python 2023")