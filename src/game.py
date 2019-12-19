import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from telegram_client import get_online_users


class PatrascheCoin:
    def __init__(self):
        self.engine = create_engine("sqlite:///patraseche_coin.sqlite")
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    @staticmethod
    def _get_random_bark():
        res = [["월월!", "멍멍!", "컹컹!"][ord(os.urandom(1)) % 3]] * 253 + ["야옹"] * 3  # 1.171875% chance of meow
        return res[ord(os.urandom(1))]

    def bark(self, update, context):
        bark = self._get_random_bark()
        if update.message.chat.id == -1001254166381:  # aquaculture group

            users = get_online_users(update.message.chat.id)  # get online users
            online_user_list = list()
            for user in users:
                online_user_list.append(user[1])
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"miners:{str(online_user_list)}\n{bark}",
                                     reply_to_message_id=update.message.message_id)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"{bark}",
                                     reply_to_message_id=update.message.message_id)
        # write balance to database
        pass

    def balance(self, update, context):
        # check if 1:1 conversation
        # read balance from database
        # send message
        pass
