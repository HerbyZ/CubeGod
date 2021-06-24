from typing import overload
from sqlalchemy import Column, Integer, BigInteger, DateTime

import datetime

from . import Base, session


class User(Base):
    __tablename__ = 'users'
    discord_id = Column(BigInteger, primary_key=True)
    join_date = Column(DateTime, default=datetime.datetime.now)
    level = Column(Integer, default=1)
    experience = Column(Integer, default=0)

    @staticmethod
    def create(discord_id, join_date=datetime.datetime.now(), level=1, exp=0):
        try:
            User.find_one(discord_id)
        except ValueError:
            user = User()
            user.discord_id = discord_id
            user.join_date = join_date
            user.level = level
            user.experience = exp
            
            session.add(user)
            session.commit()
            session.close()

            return User.find_one(discord_id)

        raise ValueError(f'User with discord id {discord_id} already exists')

    @staticmethod
    def find_one(discord_id):
        user = session.query(User).filter(User.discord_id == discord_id).first()
        if user is None:
            raise ValueError(f'User with discord id {discord_id} not found')

        return user

    @staticmethod
    def update(discord_id, **kwargs):
        session.query(User).filter(User.discord_id == discord_id).update(kwargs)

    @staticmethod
    def delete(discord_id):
        session.query(User).filter(User.discord_id == discord_id).delete()
