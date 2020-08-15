import os
import random
import re
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import telegram

from models.daily_lottery import User, BuyLog

PATRASCHE_ROOTDIR = os.getenv('PATRASCHE_ROOTDIR')
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

bot = telegram.Bot(TELEGRAM_API_TOKEN)

MEOW_GROUP_ID = -1001265183135
TICKET_PRICE = 1000


class DailyLottery:
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
        first = ""
        second = ""
        third = ""
        fourth = ""
        tickets = self.session.query(BuyLog.account_id, BuyLog.number).all()
        patrasche = self.session.query(User).filter(User.account_id == "patrasche").one()
        for ticket in tickets:  # current EV: .795
            user = self.session.query(User).filter(User.account_id == ticket.account_id).one()
            if ticket.number == number:  # pay 1st prize
                first += f"<b>{ticket.number}</b> - {user.name}\n"
                user.balance += TICKET_PRICE * 300
                patrasche.balance -= TICKET_PRICE * 300
            elif ticket.number[1:] == number[1:]:  # pay 2nd prize
                second += f"{ticket.number[:1]}<b>{ticket.number[1:]}</b> - {user.name}\n"
                user.balance += TICKET_PRICE * 100
                patrasche.balance -= TICKET_PRICE * 100
            elif ticket.number[2:] == number[2:]:  # pay 3rd prize
                third += f"{ticket.number[:2]}<b>{ticket.number[2:]}</b> - {user.name}\n"
                user.balance += TICKET_PRICE * 25
                patrasche.balance -= TICKET_PRICE * 25
            elif ticket.number[3:] == number[3:]:  # pay 4th prize
                fourth += f"{ticket.number[:3]}<b>{ticket.number[3:]}</b> - {user.name}\n"
                user.balance += TICKET_PRICE * 5
                patrasche.balance -= TICKET_PRICE * 5
            else:  # pay 5th prize
                user.balance += TICKET_PRICE * 0
            self.session.add(user)

        self.session.query(BuyLog).delete()
        self.session.commit()

        msg = "[일일복권 결과]\n"
        msg += "[1등상]\n"
        msg += f"{first if first else '-'}\n"
        msg += "[2등상]\n"
        msg += f"{second if second else '-'}\n"
        msg += "[3등상]\n"
        msg += f"{third if third else '-'}\n"
        msg += "[4등상]\n"
        msg += f"{fourth if fourth else '-'}\n"
        bot.send_message(MEOW_GROUP_ID, msg, parse_mode="HTML")

    def print_balance(self, update, context):
        if update.message.chat.id == MEOW_GROUP_ID:
            msg = "[개인잔고]\n"
            users = self.session.query(User).order_by(User.name).all()
            for user in users:
                msg += f"{user.name}: {user.balance:,} Ᵽ\n"
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=msg,
                                     reply_to_message_id=update.message.message_id,
                                     parse_mode='html')

    def _take_ptc(self, current_user, amount):
        patrasche = self.session.query(User).filter(User.account_id == "patrasche").one()
        if current_user.balance >= amount:
            current_user.balance -= amount
            patrasche.balance += amount
            self.session.add(current_user)
            self.session.add(patrasche)
        else:
            if random.random() > 0.8:
                message = "돈없으면 꺼져"
            else:
                message = "잔고가 부족합니다"
            bot.send_message(MEOW_GROUP_ID, message)
            raise ValueError

    def buy_lottery(self, update, context):
        if update.message.chat.id == MEOW_GROUP_ID:
            current_user = self.session.query(User).filter(User.account_id == str(update.message.from_user.id)).one()
            try:
                if update.message.text.split(" ")[0] in ['/a', '/auto'] and re.fullmatch(r"^[1-9]\d*$", context.args[0]):  # purchase tickets with random number
                    num_tickets = int(context.args[0])
                    self._take_ptc(current_user, TICKET_PRICE * num_tickets)
                    numbers = []
                    for _ in range(num_tickets):
                        numbers += [self._spin_lottery()]
                elif update.message.text in ['/a', '/auto']:
                    context.bot.send_message(chat_id=update.effective_chat.id,
                                             text="1 이상의 정수를 입력해주세요",
                                             reply_to_message_id=update.message.message_id,
                                             parse_mode='html')
                    return
                elif re.fullmatch(r"^[0-9]{4}(?: [0-9]{4})*$", ' '.join(context.args[0:])):  # purchase multiple tickets
                    numbers = context.args[0:]
                    self._take_ptc(current_user, TICKET_PRICE * len(numbers))
                else:
                    context.bot.send_message(chat_id=update.effective_chat.id,
                                             text="4자리 숫자를 입력해주세요 0000~9999",
                                             reply_to_message_id=update.message.message_id,
                                             parse_mode='html')
                    return
            except ValueError:
                return

            for number in numbers:
                new_ticket = BuyLog(update.message.from_user.id, number)
                self.session.add(new_ticket)

            self.session.commit()
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"{' '.join(numbers)} 구매 완료\n잔고: {current_user.balance} Ᵽ",
                                     reply_to_message_id=update.message.message_id,
                                     parse_mode='html')

        else:
            pass

    def run_lottery(self):
        bot.send_message(MEOW_GROUP_ID, f"5초 후에 추첨을 시작합니다.")
        time.sleep(5)

        number = self._spin_lottery()
        bot.send_message(MEOW_GROUP_ID, f"<b>{number}</b>", parse_mode="HTML")

        self._pay_lottery(number)

        bot.send_message(MEOW_GROUP_ID, f"끝")

    def list_tickets(self):
        pass
