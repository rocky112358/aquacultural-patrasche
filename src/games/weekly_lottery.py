import os
import re

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

PATRASCHE_ROOTDIR = os.getenv('PATRASCHE_ROOTDIR')
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

MEOW_GROUP_ID = -1001265183135


class WeeklyLottery:
    def __init__(self):
        if PATRASCHE_ROOTDIR is None:
            print("ERROR: Set PATRASCHE_ROOTDIR")
            exit(1)
        self.engine = create_engine(f"sqlite:///{PATRASCHE_ROOTDIR}weekly_lottery.sqlite")
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def _spin_lottery(self):
        pass

    def _pay_lottery(self):
        pass

    @staticmethod
    def buy_lottey(self, update, context):
        if update.message.chat.id == MEOW_GROUP_ID:
            if len(context.args) != 1 or (not re.fullmatch(r"[0-9]{4}", context.args[0])):
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="4자리 숫자를 입력해주세요 0000~9999",
                                         reply_to_message_id=update.message.message_id,
                                         parse_mode='html')
                return
            number = context.args[0]
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"{number} 구매 완료",
                                     reply_to_message_id=update.message.message_id,
                                     parse_mode='html')

        else:
            pass

    def run_lottery(self):
        pass
