import os
import time

import telegram

from game import PatrascheCoin

TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

bot = telegram.Bot(TELEGRAM_API_TOKEN)

if __name__ == '__main__':
    patrasche_coin = PatrascheCoin()

    patrasche = patrasche_coin.get_info("patrasche")
    if patrasche_coin.balance >= 126000 * 5:
        patrasche_coin.airdrop()

    users = patrasche_coin.get_all_info()

    message_text = ""
    for user in users:
        message_text += f"{user.name}(rank: {user.meow_count}): {user.balance}\n"

    bot.send_message(-1001265183135, message_text)
