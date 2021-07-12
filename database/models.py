from sqlalchemy.orm import relationship
from sqlalchemy.orm.attributes import set_attribute
from sqlalchemy import Column, Integer, String, BigInteger, DateTime, ForeignKey, Text, Boolean, update, desc

import datetime

from . import Base, session, engine


class Ban(Base):
    __tablename__ = 'bans'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.discord_id'))
    user = relationship('User', back_populates='bans')
    date = Column(DateTime, default=datetime.datetime.now)
    is_active = Column(Boolean, default=True)
    reason = Column(Text, nullable=True)

    def set_inactive(self):
        with session() as s:
            s.execute(
                update(Ban).
                where(Ban.id == self.id).
                values(is_active=False)
            )
            s.commit()

        self.is_active = False


class Imprisonment(Base):
    __tablename__ = 'imprisonments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.discord_id'))
    user = relationship('User', back_populates='imprisonments')
    date = Column(DateTime, default=datetime.datetime.now)
    is_active = Column(Boolean, default=True)
    reason = Column(Text, nullable=True)

    def set_inactive(self):
        with session() as s:
            s.execute(
                update(Imprisonment).
                where(Imprisonment.id == self.id).
                values(is_active=False)
            )
            s.commit()

        self.is_active = False


class User(Base):
    __tablename__ = 'users'
    discord_id = Column(BigInteger, primary_key=True)
    join_date = Column(DateTime, default=datetime.datetime.now)
    level = Column(Integer, default=1)
    experience = Column(Integer, default=0)
    bans = relationship('Ban', back_populates='user', cascade='all, delete-orphan', lazy='joined',
                        order_by=lambda: desc(Ban.date))
    imprisonments = relationship('Imprisonment', back_populates='user', cascade='all, delete-orphan',
                                 lazy='joined', order_by=lambda: desc(Imprisonment.date))
    is_banned = Column(Boolean, default=False)
    is_prisoned = Column(Boolean, default=False)

    def update(self, **kwargs):
        with session() as s:
            for key, value in kwargs.items():
                set_attribute(self, key, value)

            s.execute(
                update(User).
                where(User.discord_id == self.discord_id).
                values(**kwargs)
            )
            s.commit()

    def ban(self, reason=None):
        if not self.is_banned:
            ban = Ban(user_id=self.discord_id, reason=reason)

            self.bans.append(ban)

            self.update(is_banned=True)

            with session() as s:
                s.add(ban)
                s.commit()
                s.refresh(self)
        else:
            raise ValueError('User is already banned')

    def unban(self):
        if self.is_banned:
            self.update(is_banned=self.is_banned)
            self.is_banned = False

            ban = self.bans[0]
            ban.set_inactive()
        else:
            raise ValueError('User is not banned')

    def get_bans(self):
        with session() as s:
            bans = s.query(Ban).filter(Ban.user_id == self.discord_id).\
                order_by(Ban.date.desc()).all()

        return bans

    def imprison(self, reason=None):
        if not self.is_prisoned and not self.is_banned:
            imprisonment = Imprisonment(user_id=self.discord_id, reason=reason)

            self.imprisonments.append(imprisonment)

            self.update(is_prisoned=True)

            with session() as s:
                s.add(imprisonment)
                s.commit()
                s.refresh(self)
        else:
            raise ValueError('User is already prisoned or banned')

    def end_imprisonment(self):
        if self.is_prisoned:
            self.update(is_prisoned=False)
            self.is_prisoned = False

            imprisonment = self.imprisonments[0]
            imprisonment.set_inactive()
        else:
            raise ValueError('User is not prisoned')

    def get_imprisonments(self):
        with session() as s:
            imprisonments = s.query(Imprisonment).filter(Imprisonment.user_id == self.discord_id).\
                order_by(Imprisonment.date.desc()).all()

        return imprisonments


Base.metadata.create_all(bind=engine)
