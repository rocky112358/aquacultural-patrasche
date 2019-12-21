import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.patrasche_coin import User
from telegram_client import get_online_users

BARK_COST = 2520  # LCM of 1~len(user_list)


class PatrascheCoin:
    def __init__(self):
        self.engine = create_engine("sqlite:///patrasche_coin.sqlite")
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    @staticmethod
    def _get_random_bark():
        res = [["월월!", "멍멍!", "컹컹!"][ord(os.urandom(1)) % 3]] * 178 \
              + ["파트라슈는 안전자산!"] * 64 \
              + ["크르릉..."] * 8 \
              + ["옹야"] * 3 \
              + ["야옹"] * 3  # 25% chance of free bark, 3.125% change of cost*1.5, 1.171875% chance of 야옹

        return res[ord(os.urandom(1))]

    def bark(self, update, context):
        if len(context.args) == 0:
            bark_count = 1
        else:
            try:
                bark_count = int(context.args[0])
            except ValueError:
                bark_count = 1

        resp_text = ""
        if update.message.chat.id == -1001254166381:  # aquaculture group
            # get a list of online users
            online_users = get_online_users(update.message.chat.id)
            # and remove from_user's id
            while update.message.from_user.id in online_users:
                online_users.remove(update.message.from_user.id)
            # and add patrasche
            online_users.append("patrasche")

            for _ in range(bark_count):
                bark = self._get_random_bark()
                # check if the user has enough balance to bark
                current_user = self.session.query(User).filter(User.id == str(update.message.from_user.id)).one()
                if (current_user.balance - BARK_COST) < 0:
                    resp_text += "check your balance\n"
                    break

                resp_text += f"{bark}\n"
                current_user.bark_count += 1

                # free bark
                if bark == "파트라슈는 안전자산!":
                    continue

                # subtract bark cost from balance
                current_user.balance -= BARK_COST
                # and give coin to miners
                for user_id in online_users:
                    mining_user = self.session.query(User).filter(User.id == str(user_id)).one()
                    mining_user.balance += BARK_COST / len(online_users)
                    self.session.add(mining_user)

                # additional cost
                if bark == "크르릉...":
                    patrasche = self.session.query(User).filter(User.id == "patrasche").one()
                    current_user.balance -= BARK_COST / 2
                    patrasche.balance += BARK_COST / 2

                # check if 야옹
                if bark == "야옹":
                    patrasche = self.session.query(User).filter(User.id == "patrasche").one()
                    prize = patrasche.balance / 2
                    patrasche.balance -= prize
                    current_user.balance += prize
                    current_user.meow_count += 1
                    resp_text += f"Reward: {prize}PTC\n"

                self.session.add(current_user)
                self.session.commit()

        else:
            bark = self._get_random_bark()
            resp_text += f"{bark}\n"

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=resp_text,
                                 reply_to_message_id=update.message.message_id)

    def balance(self, update, context):
        # check if 1:1 conversation
        # read balance from database
        # send message
        pass
