from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer

Base = declarative_base()


class User(Base):
    __tablename__ = 'user_balance'

    account_id = Column(Integer, primary_key=True)
    balance = Column(Integer)


class BuyLog(Base):
    __tablename__ = 'tickets'

    account_id = Column(Integer)
    number = Column(Integer)

    def __init__(self, account_id, number):
        self.account_id = account_id
        self.number = number
