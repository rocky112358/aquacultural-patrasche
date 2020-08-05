import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api import send_message
from models.daily_lottery import User

PATRASCHE_ROOTDIR = os.getenv('PATRASCHE_ROOTDIR')

engine = create_engine(f"sqlite:///{PATRASCHE_ROOTDIR}weekly_lottery.sqlite")
Session = sessionmaker(bind=engine)
session = Session()

BASIC_INCOME_AMOUNT = 1000


def pay_basic_income():
    patrasche = session.query(User).filter(User.account_id == 0).one()
    users = session.query(User).all()
    if patrasche.balance >= BASIC_INCOME_AMOUNT * len(users):
        patrasche.balance -= BASIC_INCOME_AMOUNT * len(users)
        for user in users:
            user.balance += BASIC_INCOME_AMOUNT
            session.add(user)
        session.add(patrasche)
        session.commit()
        send_message(f"[기본소득] 지급완료")
    else:
        send_message(f"[기본소득] 잔고부족")


if __name__ == '__main__':
    pay_basic_income()
