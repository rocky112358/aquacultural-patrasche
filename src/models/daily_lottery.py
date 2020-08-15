from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    account_id = Column(Integer, primary_key=True)
    balance = Column(Integer)
    name = Column(String)
    total_ticket = Column(Integer)
    total_prize = Column(Integer)


class BuyLog(Base):
    __tablename__ = 'tickets'

    fake_pk = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer)
    number = Column(Integer)

    def __init__(self, account_id, number):
        self.account_id = account_id
        self.number = number
