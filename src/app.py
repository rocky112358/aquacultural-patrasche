from collections import defaultdict
from datetime import datetime, timedelta
import logging
import os
import random

from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.filters import Filters
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
    else:
        resp_text = random.randint(1, dice_face_cnt)
    context.bot.send_message(chat_id=update.effective_chat.id, text=resp_text,
                             reply_to_message_id=update.message.message_id)


def tf(update, context):
    resp_text = random.sample(['응', '아니'], 1)[0]
    context.bot.send_message(chat_id=update.effective_chat.id, text=resp_text,
                             reply_to_message_id=update.message.message_id)


def _get_random_bark():
    res = [["월월!", "멍멍!", "컹컹!"][ord(os.urandom(1)) % 3]] * 255 \
          + ["야옹"] * 1

    return res[ord(os.urandom(1))]


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


del_candidate = defaultdict(lambda: {"voters": set(), "expire": datetime.now()})
del_notice_list = ["삭제했다 애송이", "삼진에바로 기각되었습니다", "파트라슈가 해치웠으니 안심하라구!"]


def del_(update, context):
    reply_message = update.message.reply_to_message
    if reply_message is not None and update.effective_chat.id == -1001254166381:
        reply_message_id = reply_message.message_id
        del_candidate[reply_message_id]["voters"].add(update.message.from_user.id)
        del_candidate[reply_message_id]["expire"] = datetime.now() + timedelta(minutes=30)
        if len(del_candidate[reply_message_id]["voters"]) >= 3:
            delete_message(-1001254166381, reply_message_id)
            context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(del_notice_list))
            del del_candidate[reply_message_id]
    del_keys = []
    for each in del_candidate.keys():
        if del_candidate[each]["expire"] < datetime.now():
            del_keys.append(each)
    for each in del_keys:
        del del_candidate[each]


mute_user_dict = defaultdict(lambda: {"voters": set(), "expire": datetime.now() + timedelta(minutes=3)})


def mute_loop(update, context):
    if update.message.from_user.id in mute_user_dict.keys():
        if mute_user_dict[update.message.from_user.id]['expire'] <= datetime.now():
            del mute_user_dict[update.message.from_user.id]
        elif len(mute_user_dict[update.message.from_user.id]["voters"]) >= 3:
            delete_message(-1001254166381, update.message.message_id)


def mute(update, context):
    reply_message = update.message.reply_to_message
    if reply_message is not None and update.effective_chat.id == -1001254166381:
        mute_user_dict[reply_message.from_user.id]["voters"].add(update.message.from_user.id)


# help command
def help_(update, context):
    resp_text = "/roll [faces], /r [faces]: [faces]개의 면을 가진 주사위를 굴립니다. 기본값 6\n" \
                "/bool, /coin, /tf: 파트라슈가 응/아니로 대답해줍니다.\n" \
                "/up: 파트라슈가 대화를 밀어올려줍니다\n" \
                "/vs [list]: /로 구분된 [list]안의 선택지 중에서 하나를 골라줍니다.\n" \
                "/del, /eva, /evande: 답글로 이렇게 달면 해당 메세지를 삭제합니다. 서로 다른 3명 필요\n" \
                "/mute: 답글로 이렇게 달면 3분간 해당 사용자의 메세지는 자동으로 지워집니다. 서로 다른 3명 필요\n"
    # a = [", ".join(each.command) for each in dispatcher.handlers[0]]
    # resp_text = ", ".join(a)
    context.bot.send_message(chat_id=update.effective_chat.id, text=resp_text)


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


# patrasche coin (closed)
# patrasche_coin = PatrascheCoin()

# handlers
roll_handler = CommandHandler(['roll', 'r'], roll)
tf_handler = CommandHandler(['bool', 'coin', 'tf'], tf)
bark_handler = CommandHandler(['bark', 'b'], bark)
up_handler = CommandHandler('up', up)
help_handler = CommandHandler('help', help_)
vs_handler = CommandHandler('vs', vs)
del_handler = CommandHandler(['del', 'eva', 'evande'], del_)
mute_handler = CommandHandler('mute', mute)
mute_loop = MessageHandler(Filters.all, mute_loop)

# add handlers to dispatcher
dispatcher.add_handler(roll_handler)
dispatcher.add_handler(tf_handler)
dispatcher.add_handler(bark_handler)
dispatcher.add_handler(up_handler)
dispatcher.add_handler(vs_handler)
dispatcher.add_handler(del_handler)
dispatcher.add_handler(mute_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(mute_loop)

# add an error handler to dispatcher
dispatcher.add_error_handler(err_handler)

updater.start_polling()
