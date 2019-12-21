from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    __tablename__ = 'aqua_user'

    id = Column(String, primary_key=True)
    balance = Column(Integer)
    meow_count = Column(Integer)
    bark_count = Column(Integer)

    def __init__(self, id, balance):
        self.id = id
        self.balance = balance
