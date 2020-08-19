import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import telegram

from models.daily_lottery import User, BuyLog

PATRASCHE_ROOTDIR = os.getenv('PATRASCHE_ROOTDIR')
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

bot = telegram.Bot(TELEGRAM_API_TOKEN)

MEOW_GROUP_ID = -1001265183135
TICKET_PRICE = 1000


class Roulette:
    def __init__(self):
        if PATRASCHE_ROOTDIR is None:
            print("ERROR: Set PATRASCHE_ROOTDIR")
            exit(1)
        self.engine = create_engine(f"sqlite:///{PATRASCHE_ROOTDIR}daily_lottery.sqlite")
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def bet(self, update, context):
        if update.message.chat.id == MEOW_GROUP_ID:
            keyboard = telegram.ReplyKeyboardMarkup([
                ["1to18", "EVEN", "RED", "BLACK", "ODD", "19to36"],
                ["1st12", "2nd12", "3rd12"],
                ["1", "4", "7", "10", "13", "16", "19", "22", "25", "28", "31", "34"],
                ["1", "4", "7", "10", "13", "16", "19", "22", "25", "28", "31", "34"],
                ["1", "4", "7", "10", "13", "16", "19", "22", "25", "28", "31", "34"],
                ["1", "4", "7", "10", "13", "16", "19", "22", "25", "28", "31", "34"],
                ["1", "4", "7", "10", "13", "16", "19", "22", "25", "28", "31", "34"],
                ["1", "4", "7", "10", "13", "16", "19", "22", "25", "28", "31", "34"],
                ["1", "4", "7", "10", "13", "16", "19", "22", "25", "28", "31", "34"],
                ["1", "4", "7", "10", "13", "16", "19", "22", "25", "28", "31", "34"],
                ["1", "4", "7", "10", "13", "16", "19", "22", "25", "28", "31", "34"],
                ["1", "4", "7", "10", "13", "16", "19", "22", "25", "28", "31", "34"],
                ["1", "4", "7", "10", "13", "16", "19", "22", "25", "28", "31", "34"],
                ["1", "4", "7", "10", "13", "16", "19", "22", "25", "28", "31", "34"],
                ["1", "4", "7", "10", "13", "16", "19", "22", "25", "28", "31", "34"],
            ])
            bot.send_message(update.message.chat.id,
                             "Bet down, please.",
                             reply_to_message_id=update.message.message_id,
                             reply_markup=keyboard)
