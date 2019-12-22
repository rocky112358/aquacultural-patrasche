import os
import time

import telegram

from game import PatrascheCoin

TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

bot = telegram.Bot(TELEGRAM_API_TOKEN)
BARK_INTERVAL = [60, 40, 20, 10, 5, 3]  # 5, 6, 7, 8, 9, 10

if __name__ == '__main__':
    patrasche_coin = PatrascheCoin()
    bark_patrasche = False
    interval = 0
    total_bark = 0

    users = patrasche_coin.get_all_info()

    message_text = ""
    for user in users:
        message_text += f"{user.name}(rank: {user.meow_count}): {user.balance}\n"
        if user.id == "patrasche" and user.balance >= 5 * 126000:
            bark_patrasche = True
            bark_interval_index = user.balance // 126000 - 5
            interval = BARK_INTERVAL[bark_interval_index]
            total_bark = 600 // interval

    bot.send_message(-1001265183135, message_text)
    if bark_patrasche:
        bot.send_message(-1001265183135, f"지금부터 ({interval})초 간격으로 ({total_bark})번 짖어보겠습니다.")
        for _ in range(total_bark):
            patrasche_coin.self_bark()
            time.sleep(interval)
