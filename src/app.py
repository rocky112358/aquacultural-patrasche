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
logging.info("bot start")


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


def _get_random_bark():
    res = [random.sample(["월월!", "멍멍!", "컹컹!"], 1)[0]] * 99 + ["야옹"]  # 1% chance of meow
    return random.sample(res, 1)[0]


def bark(update, context):
    resp_text = _get_random_bark()
    context.bot.send_message(chat_id=update.effective_chat.id, text=resp_text,
                             reply_to_message_id=update.message.message_id)


def up(update, context):
    resp_text = f".\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n" \
                f"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n{_get_random_bark()}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=resp_text,
                             reply_to_message_id=update.message.message_id)


def vs(update, context):
    if len(context.args) == 0:
        return  # no answer for trolls
    vs_string = " ".join(context.args)
    vs_list = list(map(lambda x: x.strip(), vs_string.split("/")))
    if len(vs_list) == 1:
        return  # no answer for trolls
    if any([len(x) == 0 for x in vs_list]):
        return  # no answer for trolls
    resp_text = random.sample(vs_list, 1)[0]
    context.bot.send_message(chat_id=update.effective_chat.id, text=resp_text,
                             reply_to_message_id=update.message.message_id)


# handlers
start_handler = CommandHandler('start', start)
roll_handler = CommandHandler('roll', roll)
bark_handler = CommandHandler('bark', bark)
up_handler = CommandHandler('up', up)
vs_handler = CommandHandler('vs', vs)

# dispatchers
dispatcher.add_handler(start_handler)
dispatcher.add_handler(roll_handler)
dispatcher.add_handler(bark_handler)
dispatcher.add_handler(up_handler)
dispatcher.add_handler(vs_handler)

updater.start_polling()
