import logging
import os
import random

from telegram.ext import Updater, CommandHandler

TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
from game import PatrascheCoin
if TELEGRAM_API_TOKEN is None:
    print("ERROR: Set TELEGRAM_API_TOKEN")
    exit(1)

# telegram setting
updater = Updater(token=TELEGRAM_API_TOKEN, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("bot start")


def start(update, context):
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


def patrasche_coin_help(update, context):
    help_text = """
    1 bark = 63PTC 소비
    채굴: bark 시 online 상태인 다른유저와 파트라슈가 63PTC를 1/n로 나눠가짐
    <확률표>
    월월!, 멍멍!, 컹컹! (69.53125%)
    파트라슈는 안전자산! (25%): 63PTC 반환, 채굴 없음
    크르릉... (3.125%): 파트라슈가 31.5PTC 추가 징수
    옹야 (1.171875%)
    야옹 (1.171875%): 야옹 카운트 +1, 파트라슈 잔고의 절반 획득
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_text,
                             reply_to_message_id=update.message.message_id)

def err_handler(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


# patrasche coin
patrasche_coin = PatrascheCoin()

# handlers
start_handler = CommandHandler('start', start)
roll_handler = CommandHandler('roll', roll)
r_handler = CommandHandler('r', roll)
bark_handler = CommandHandler('bark', patrasche_coin.bark)
up_handler = CommandHandler('up', up)
vs_handler = CommandHandler('vs', vs)
ptchelp_handler = CommandHandler('ptchelp', patrasche_coin_help)

# add handlers to dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(roll_handler)
dispatcher.add_handler(r_handler)
dispatcher.add_handler(bark_handler)
dispatcher.add_handler(up_handler)
dispatcher.add_handler(vs_handler)
dispatcher.add_handler(ptchelp_handler)


# help command
def help_(update, context):
    a = [each.command[0] for each in dispatcher.handlers[0]]
    resp_text = ", ".join(a)
    context.bot.send_message(chat_id=update.effective_chat.id, text=resp_text,
                             reply_to_message_id=update.message.message_id)


help_handler = CommandHandler('help', help_)
dispatcher.add_handler(help_handler)

# add an error handler to dispatcher
dispatcher.add_error_handler(err_handler)

updater.start_polling()
