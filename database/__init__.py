from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.session import sessionmaker

import config

engine = create_engine(config.DATABASE_CONNECTION_STRING, encoding='utf-8')
session = sessionmaker(bind=engine)

Base = declarative_base()
