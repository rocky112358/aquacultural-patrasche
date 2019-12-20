import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.patrasche_coin import User
from telegram_client import get_online_users

BARK_COST = 63


class PatrascheCoin:
    def __init__(self):
        self.engine = create_engine("sqlite:///patrasche_coin.sqlite")
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    @staticmethod
    def _get_random_bark():
        res = [["월월!", "멍멍!", "컹컹!", "파트라슈는 안전자산!"][ord(os.urandom(1)) % 4]] * 250 \
              + ["옹야"] * 3 \
              + ["야옹"] * 3  # 1.171875% chance of 야옹

        return res[ord(os.urandom(1))]

    def bark(self, update, context):
        bark = self._get_random_bark()
        resp_text = f"{bark}"

        if update.message.chat.id == -1001254166381:  # aquaculture group
            # check if the user has enough balance to bark
            current_user = self.session.query(User).filter(User.id == str(update.message.from_user.id)).one()
            if (current_user.balance - BARK_COST) < 0:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=f"check your balance",
                                         reply_to_message_id=update.message.message_id)
                return

            # get a list of online users
            online_users = get_online_users(update.message.chat.id)
            # and remove from_user's id
            while update.message.from_user.id in online_users:
                online_users.remove(update.message.from_user.id)
            # and add patrasche
            online_users.append("patrasche")

            # subtract bark cost from balance
            current_user.balance -= BARK_COST
            # and give coin to miners
            for user_id in online_users:
                mining_user = self.session.query(User).filter(User.id == str(user_id)).one()
                mining_user.balance += BARK_COST / len(online_users)
                self.session.add(mining_user)

            # check if 야옹
            if bark == "야옹":
                patrasche = self.session.query(User).filter(User.id == "patrasche").one()
                patrasche.balance = patrasche.balance / 2
                current_user.balance += patrasche.balance / 2
                current_user.meow_count += 1
                resp_text += f"\nReward: {patrasche.balance / 2}PTC"

            self.session.add(current_user)
            self.session.commit()

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=resp_text,
                                 reply_to_message_id=update.message.message_id)
        return

    def balance(self, update, context):
        # check if 1:1 conversation
        # read balance from database
        # send message
        pass
