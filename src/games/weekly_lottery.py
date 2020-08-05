import os
import random
import re
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api import send_message
from models.weekly_lottery import User, BuyLog

PATRASCHE_ROOTDIR = os.getenv('PATRASCHE_ROOTDIR')
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

MEOW_GROUP_ID = -1001265183135
TICKET_PRICE = 100


class WeeklyLottery:
    def __init__(self):
        if PATRASCHE_ROOTDIR is None:
            print("ERROR: Set PATRASCHE_ROOTDIR")
            exit(1)
        self.engine = create_engine(f"sqlite:///{PATRASCHE_ROOTDIR}weekly_lottery.sqlite")
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    @staticmethod
    def _spin_lottery():
        result = str(random.choice(range(10)))
        result += str(random.choice(range(10)))
        result += str(random.choice(range(10)))
        result += str(random.choice(range(10)))
        return result

    def _pay_lottery(self, number):
        tickets = self.session.query(BuyLog.account_id, BuyLog.number).all()
        for ticket in tickets:  # current EV: 1.05
            user = self.session.query(User).filter(User.account_id == ticket.account_id).one()
            if ticket.number == number:  # pay 1st prize
                user.balance += TICKET_PRICE * 195
            elif ticket.number[1:] == number[1:]:  # pay 2nd prize
                user.balance += TICKET_PRICE * 25
            elif ticket.number[2:] == number[2:]:  # pay 3rd prize
                user.balance += TICKET_PRICE * 12
            elif ticket.number[3:] == number[3:]:  # pay 4th prize
                user.balance += TICKET_PRICE * 5
            else:  # pay 5th prize
                user.balance += TICKET_PRICE * 0.5
            self.session.add(user)

        self.session.query(BuyLog).delete()
        self.session.commit()

    def buy_lottery(self, update, context):
        if update.message.chat.id == MEOW_GROUP_ID:
            if len(context.args) != 1 or (not re.fullmatch(r"[0-9]{4}", context.args[0])):
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="4자리 숫자를 입력해주세요 0000~9999",
                                         reply_to_message_id=update.message.message_id,
                                         parse_mode='html')
                return
            number = context.args[0]
            current_user = self.session.query(User).filter(User.account_id == str(update.message.from_user.id)).one()
            if current_user and current_user.balance >= TICKET_PRICE:
                current_user.balance -= TICKET_PRICE
            else:
                if random.random() > 0.8:
                    message = "돈없으면 꺼져"
                else:
                    message = "구매 불가"
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=message,
                                         reply_to_message_id=update.message.message_id,
                                         parse_mode='html')
                return
            new_ticket = BuyLog(update.message.from_user.id, number)

            self.session.add(current_user)
            self.session.add(new_ticket)
            self.session.commit()
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"{number} 구매 완료\n잔고: {current_user.balance} Ᵽ",
                                     reply_to_message_id=update.message.message_id,
                                     parse_mode='html')

        else:
            pass

    def run_lottery(self):
        send_message(f"5초 후에 추첨을 시작합니다.")
        time.sleep(5)
        number = self._spin_lottery()
        send_message(f"<b>{number}</b>")
        self._pay_lottery(number)
        users = self.session.query(User).all()
        msg = ""
        for each in users:
            msg += f"{each.name}: {each.balance} Ᵽ\n"
        send_message(msg)
        send_message(f"끝")

    def list_tickets(self):
        pass
