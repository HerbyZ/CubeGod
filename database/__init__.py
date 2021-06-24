from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.session import Session, sessionmaker

import config

engine = create_engine(config.DATABASE_CONNECTION_STRING, encoding='utf-8')
session: Session = sessionmaker(bind=engine)()

Base = declarative_base()

from . import models

Base.metadata.create_all(bind=engine)
