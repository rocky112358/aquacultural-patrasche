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
                ["1to12", "2nd12", "3rd12"],
                ["1stCol", " ", "2ndCol", " ", "3rdCol"],
                ["0", "TNB0-00", "00"],
                ["FiveNumberBet"],
                ["Str1-3", "1", "TNB1-2", "2", "TNB2-3", "3"],
                ["Cor1-6", "TNB1-4", "FNB1-2-4-5", "TNB2-5", "FNB2-3-5-6", "TNB3-6"],
                ["Str4-6", "4", "TNB4-5", "5", "TNB5-6", "6"],
                ["Cor4-9", "TNB4-7", "FNB4-5-7-8", "TNB5-8", "FNB5-6-8-9", "TNB6-9"],
                ["Str7-9", "7", "TNB7-8", "8", "TNB8-9", "9"],
                ["Cor7-12", "TNB7-10", "FNB7-8-10-11", "TNB8-11", "FNB8-9-11-12", "TNB9-12"],
                ["Str10-12", "10", "TNB10-11", "11", "TNB11-12", "12"],
                ["Cor10-15", "TNB10-13", "FNB10-11-13-14", "TNB11-14", "FNB11-12-14-15", "TNB12-15"],
                ["Str13-15", "13", "TNB13-14", "14", "TNB14-15", "15"],
                ["Cor13-18", "TNB13-16", "FNB13-14-16-17", "TNB14-17", "FNB14-15-17-18", "TNB15-18"],
                ["Str16-18", "16", "TNB16-17", "17", "TNB17-18", "18"],
                ["Cor16-21", "TNB16-19", "FNB16-17-19-20", "TNB5-8", "FNB17-18-20-21", "TNB18-21"],
                ["Str19-21", "19", "TNB19-20", "20", "TNB20-21", "21"]
            ])
            bot.send_message(update.message.chat.id,
                             "Bet down, please.",
                             reply_to_message_id=update.message.message_id,
                             reply_markup=keyboard)
