from sqlalchemy.orm.attributes import set_attribute
from sqlalchemy import update

from .models import User
from . import session


class UserManager:
    @staticmethod
    def create(discord_id, **kwargs) -> User:
        with session() as s:
            user = User(discord_id=discord_id)
            s.add(user)

            if kwargs:
                s.execute(
                    update(User).
                    where(User.discord_id == discord_id).
                    values(**kwargs)
                )

            s.commit()
            s.refresh(user)

        for key, value in kwargs.items():
            set_attribute(user, key, value)

        return user

    @staticmethod
    def find_one(attributes) -> User:
        with session() as s:
            user = s.get(User, attributes)

        if user is None:
            raise ValueError(f'User not found')

        return user

    @staticmethod
    def update(discord_id, **kwargs) -> User:
        user = UserManager.find_one(discord_id)

        for key, value in kwargs.items():
            set_attribute(user, key, value)

        with session() as s:
            s.execute(
                update(User).
                where(User.discord_id == discord_id).
                values(**kwargs)
            )
            s.commit()

        return user

    @staticmethod
    def delete(user_attributes):
        user = UserManager.find_one(user_attributes)

        with session() as s:
            s.delete(user)
            s.commit()
