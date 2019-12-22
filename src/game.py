import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import telegram

from models.patrasche_coin import User
from telegram_client import get_online_users, set_user_rank

BARK_COST = 2520  # LCM of 1~len(user_list)
RANK = ["0. ", "1.길냥이", "2.뚱냥이", "3.떼껄룩", "4.점박냥", "5.고등어냥", "6.치즈냥", "7.삼색냥", "8.샴고양이", "9.페르시안"] \
       + ["X.개냥이"] * 191  # 0~200 ranks
PATRASCHE_ROOTDIR = os.getenv('PATRASCHE_ROOTDIR')
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

MEOW_GROUP_ID = -1001265183135

class PatrascheCoin:
    def __init__(self):
        if PATRASCHE_ROOTDIR is None:
            print("ERROR: Set PATRASCHE_ROOTDIR")
            exit(1)
        self.engine = create_engine(f"sqlite:///{PATRASCHE_ROOTDIR}patrasche_coin.sqlite")
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    @staticmethod
    def _get_random_bark():
        res = [["월월!", "멍멍!", "컹컹!"][ord(os.urandom(1)) % 3]] * 180 \
              + ["파트라슈는 안전자산!"] * 64 \
              + ["크르릉..."] * 8 \
              + ["옹야"] * 2 \
              + ["야옹"] * 2  # 25% chance of free bark, 3.125% change of cost*1.5, 0.78125‬% chance of 야옹

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
        if update.message.chat.id == MEOW_GROUP_ID:  # meow group
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
                    initial_balance = patrasche.balance
                    prize = patrasche.balance // 2
                    patrasche.balance = initial_balance - prize
                    current_user.balance += prize
                    current_user.meow_count += 1
                    resp_text += f"<b>Reward: {prize}PTC</b>\n"

                self.session.add(current_user)
                self.session.commit()

            # get rank
            current_user = self.session.query(User).filter(User.id == str(update.message.from_user.id)).one()
            resp_text += f"RANK: [{RANK[current_user.meow_count]}]\n"
            set_user_rank(update.message.chat.id, update.message.from_user.id, RANK[current_user.meow_count])

            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=resp_text,
                                     reply_to_message_id=update.message.message_id,
                                     parse_mode='html')

        else:
            pass

    def airdrop(self):
        patrasche = self.session.query(User).filter(User.id == "patrasche").one()
        users = self.session.query(User).filter(User.id != "patrasche").all()

        result = []
        for user in users:
            if ord(os.urandom(1)) >= 128:
                result.append((user.id, user.name))

        resp_text = f"<b>Airdrop (각 10 bark)</b>\n받은사람: "
        if len(result) > 0:
            total_price = 0
            for user in result:
                u = self.session.query(User).filter(User.id == user[0]).one()
                price = BARK_COST * 10
                total_price += price
                u.balance += price
                self.session.add(u)
            patrasche.balance -= total_price
            self.session.add(patrasche)
            self.session.commit()

            resp_text += f"{', '.join([user[1] for user in result])}"

        else:
            pass

        bot = telegram.Bot(TELEGRAM_API_TOKEN)
        bot.send_message(MEOW_GROUP_ID, resp_text, parse_mode="html")

    def balance(self, update, context):
        # check if 1:1 conversation
        # read balance from database
        # send message
        pass

    def get_info(self, user_id):
        user = self.session.query(User).filter(User.id == str(user_id)).one()
        return user

    def get_all_info(self):
        users = self.session.query(User).order_by(User.balance.desc()).all()
        return users
