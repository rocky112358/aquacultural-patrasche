from datetime import datetime
import os

import requests

BOT_TOKEN = os.getenv('TELEGRAM_API_TOKEN')


def send_message(text: str):
    data = {"chat_id": -1001265183135,
            "text": text,
            "parse_mode": "HTML"}

    resp = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data=data)
    #print(resp.json())
