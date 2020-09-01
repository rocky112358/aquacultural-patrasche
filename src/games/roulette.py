import os
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import telegram

from models.daily_lottery import User, BuyLog

PATRASCHE_ROOTDIR = os.getenv('PATRASCHE_ROOTDIR')
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

bot = telegram.Bot(TELEGRAM_API_TOKEN)

MEOW_GROUP_ID = -1001265183135
TICKET_PRICE = 1000

wheel = ["00"] + list(map(lambda x: str(x), range(37)))
red = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
black = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]


class Roulette:
    def __init__(self):
        if PATRASCHE_ROOTDIR is None:
            print("ERROR: Set PATRASCHE_ROOTDIR")
            exit(1)
        self.engine = create_engine(f"sqlite:///{PATRASCHE_ROOTDIR}daily_lottery.sqlite")
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    @staticmethod
    def _spin_roulette():
        return random.choice(wheel)

    @staticmethod
    def _pay(number):
        if number in ["0", "00"]:
            pass
            return  # pay 0, 00, 0-00, FiveNumberBet
        number = int(number)
        ## pay 1 to 1
        # even / odd
        if number % 2 == 0:
            pass  # pay even
        else:
            pass  # pay odd
        # red / black:
        if number in red:
            pass  # pay red
        else:
            pass  # pay black
        # upper / lower:
        if number >= 19:
            pass  # pay upper
        else:
            pass  # pay lower

        ## pay 2 to 1
        # dozen
        if 1 <= number <= 12:
            pass  # pay 1st12
        elif 13 <= number <= 25:
            pass  # pay 2nd12
        else:
            pass  # pay 3rd12
        # column
        if number % 3 == 1:
            pass  # pay 1stCol
        elif number % 3 == 2:
            pass  # pay 2ndCol
        else:
            pass  # pay 3rdCol

        ## pay 5 to 1
        # if number >= 4 and () <= number <= ():
        #     pass  # pay upper 6
        # if number <= 33 and () <= number <= ():
        #     pass  # pay lower 6

        ## pay 6 to 1
        # if number in [1, 2, 3]:
        #     pass  # pay FiveNumberBet

        ## pay 8 to 1

    @staticmethod
    def _pick_number():
        return random.choice(wheel)

    def play_game(self):
        number = self._pick_number()
        self._pay(number)
        return

    def bet(self, update, context):
        if update.message.chat.id == MEOW_GROUP_ID:
            keyboard = telegram.ReplyKeyboardMarkup([
                ["End Betting"],
                ["1to18", "EVEN", "RED🟥", "BLACK⬛️", "ODD", "19to36"],
                ["1to12", "2nd12", "3rd12"],
                [" ""1stCol", " ", "2ndCol", " ", "3rdCol"],
                ["0", "0-00", "00"],
                ["FiveNumberBet"],
                ["S1-3", "1🟥", "1-2", "2⬛️", "2-3", "3🟥"],
                ["C1-6", "1-4", "1-2-4-5", "2-5", "2-3-5-6", "3-6"],
                ["S4-6", "4⬛️", "4-5", "5🟥", "5-6", "6⬛️"],
                ["C4-9", "4-7", "4-5-7-8", "5-8", "5-6-8-9", "6-9"],
                ["S7-9", "7🟥", "7-8", "8⬛️", "8-9", "9🟥"],
                ["C7-12", "7-10", "7-8-10-11", "8-11", "8-9-11-12", "9-12"],
                ["S10-12", "10⬛️", "10-11", "11⬛️", "11-12", "12🟥"],
                ["C10-15", "10-13", "10-11-13-14", "11-14", "11-12-14-15", "12-15"],
                ["S13-15", "13⬛️", "13-14", "14🟥", "14-15", "15⬛️"],
                ["C13-18", "13-16", "13-14-16-17", "14-17", "14-15-17-18", "15-18"],
                ["S16-18", "16🟥", "16-17", "17⬛️", "17-18", "18🟥"],
                ["C16-21", "16-19", "16-17-19-20", "17-20", "17-18-20-21", "18-21"],
                ["S19-21", "19🟥", "19-20", "20⬛️", "20-21", "21🟥"],
                ["C19-24", "19-22", "19-20-22-23", "20-23", "20-21-23-24", "21-24"],
                ["S22-24", "22⬛️", "22-23", "23🟥", "23-24", "24⬛️"],
                ["C22-27", "22-25", "22-23-25-26", "23-26", "23-24-26-27", "24-27"],
                ["S25-27", "25🟥", "25-26", "26⬛️", "26-27", "27🟥"],
                ["C25-30", "25-28", "25-26-28-29", "26-29", "26-27-29-30", "27-30"],
                ["S28-30", "28⬛️", "28-29", "29⬛️", "29-30", "30🟥"],
                ["C28-33", "28-31", "28-29-31-32", "29-32", "29-30-32-33", "30-33"],
                ["S31-33", "31⬛️", "31-32", "32🟥", "32-33", "33⬛️"],
                ["C31-36", "31-34", "31-32-34-35", "32-35", "32-33-35-36", "33-36"],
                ["S34-36", "34🟥", "34-35", "35⬛️", "35-36", "36🟥"]
            ])
            print(update.message.text)
            if update.message.text != "End Betting":
                if update.message.text != '/bet':
                    bot.send_message(update.message.chat.id,
                                     f"Bet {update.message.text}",
                                     reply_to_message_id=update.message.message_id,
                                     reply_markup=keyboard)
                bot.send_message(update.message.chat.id,
                                 "Bet down, please.",
                                 reply_to_message_id=update.message.message_id,
                                 reply_markup=keyboard)
                return "betting"
            else:
                return "end"

    def bet_end(self, update, context):
        bot.send_message(update.message.chat.id,
                         "Good luck!",
                         reply_to_message_id=update.message.message_id,
                         reply_markup=telegram.ReplyKeyboardRemove)