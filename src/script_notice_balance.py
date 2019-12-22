import os

import telegram

from game import PatrascheCoin

TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

bot = telegram.Bot(TELEGRAM_API_TOKEN)

if __name__ == '__main__':
    patrasche_coin = PatrascheCoin()
    bark_patrasche = False

    users = patrasche_coin.get_all_info()

    message_text = ""
    for user in users:
        message_text += f"{user.name}(rank: {user.meow_count}): {user.balance}\n"
        if user.id == "patrasche" and user.balance >= 5 * 126000:
            bark_patrasche = True

    bot.send_message(-1001265183135, message_text)
    if bark_patrasche:
        bot.send_message(-1001265183135, "지금부터 좀 짖어보겠습니다.")
