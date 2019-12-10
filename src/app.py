import logging
import random

from telegram.ext import Updater, CommandHandler

TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
if TELEGRAM_API_TOKEN is None:
    print("ERROR: Set TELEGRAM_API_TOKEN")
    exit(1)

# telegram setting
updater = Updater(token=TELEGRAM_API_TOKEN, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(update, context):
    print(update)
    print(context)
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def roll(update, context):
    # find the number of faces
    if len(context.args) == 0:
        dice_face_cnt = 6
    else:
        try:
            dice_face_cnt = int(context.args[0])
        except ValueError:
            dice_face_cnt = 6

    # roll
    if dice_face_cnt < 2:  # boom!
        resp_text = "월월!"
    elif dice_face_cnt == 2:  # coin flip
        resp_text = random.sample(['응', '아니'], 1)[0]
    else:
        resp_text = random.randint(1, dice_face_cnt)
    context.bot.send_message(chat_id=update.effective_chat.id, text=resp_text,
                             reply_to_message_id=update.message.message_id)


def bark(update, context):
    resp_text = random.sample(["월월!", "멍멍!", "컹컹!"], 1)[0]
    context.bot.send_message(chat_id=update.effective_chat.id, text=resp_text,
                             reply_to_message_id=update.message.message_id)


start_handler = CommandHandler('start', start)
roll_handler = CommandHandler('roll', roll)
bark_handler = CommandHandler('bark', bark)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(roll_handler)
dispatcher.add_handler(bark_handler)

updater.start_polling()
