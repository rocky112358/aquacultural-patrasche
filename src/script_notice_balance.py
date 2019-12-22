import os
import time

import telegram

from game import PatrascheCoin

TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

bot = telegram.Bot(TELEGRAM_API_TOKEN)

if __name__ == '__main__':
    patrasche_coin = PatrascheCoin()
    bark_patrasche = False
    interval = 0
    total_bark = 0

    users = patrasche_coin.get_all_info()

    message_text = ""
    for user in users:
        message_text += f"{user.name}(rank: {user.meow_count}): {user.balance}\n"

    bot.send_message(-1001265183135, message_text)
    patrasche_coin.airdrop()
