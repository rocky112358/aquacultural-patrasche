from collections import defaultdict
from datetime import datetime, timedelta
import logging
import os
import random

from telegram.ext import Updater, CommandHandler
from telegram_client import delete_message

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


def _get_random_bark():
    res = [["월월!", "멍멍!", "컹컹!"][ord(os.urandom(1)) % 3]] * 255 \
          + ["야옹"] * 1

    return res[ord(os.urandom(1))]


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


del_candidate = defaultdict(lambda: {"voters": set(), "expire": datetime.now()})


def del_(update, context):
    reply_message = update.message.reply_to_message
    if reply_message is not None and update.effective_chat.id == -1001254166381:
        reply_message_id = reply_message.message_id
        del_candidate[reply_message_id]["voters"].add(update.message.from_user.id)
        del_candidate[reply_message_id]["expire"] = datetime.now()+timedelta(minutes=30)
        if len(del_candidate[reply_message_id]["voters"]) >= 3:
            delete_message(-1001254166381, reply_message_id)
            context.bot.send_message(chat_id=update.effective_chat.id, text="삭제했다 애송이")
            del del_candidate[reply_message_id]
    del_keys = []
    for each in del_candidate.keys():
        if del_candidate[each]["expire"] < datetime.now():
            del_keys.append(each)
    for each in del_keys:
        del del_candidate[each]


def patrasche_coin_help(update, context):
    help_text = """
1 bark = 2520PTC 소비
채굴: bark 시 online 상태인 다른유저와 파트라슈가 2520PTC를 1/n로 나눠가짐

<확률표>
월월!, 멍멍!, 컹컹! (70.3125%)
파트라슈는 안전자산! (25%): 2520PTC 반환, 채굴 없음
크르릉... (3.125%): 파트라슈가 1260PTC(1/2 bark) 추가 징수
옹야 (0.78125%)
야옹 (0.78125%): 야옹 카운트 +1, 파트라슈 잔고의 절반 획득
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
b_handler = CommandHandler('b', patrasche_coin.bark)
up_handler = CommandHandler('up', up)
vs_handler = CommandHandler('vs', vs)
ptchelp_handler = CommandHandler('ptchelp', patrasche_coin_help)
del_handler = CommandHandler('del', del_)

# add handlers to dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(roll_handler)
dispatcher.add_handler(r_handler)
dispatcher.add_handler(bark_handler)
dispatcher.add_handler(b_handler)
dispatcher.add_handler(up_handler)
dispatcher.add_handler(vs_handler)
dispatcher.add_handler(ptchelp_handler)
dispatcher.add_handler(del_handler)


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
