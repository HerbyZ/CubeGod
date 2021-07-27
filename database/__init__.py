from mongoengine import connect

import config


def init():
    connect(host=config.DATABASE_CONNECTION_STRING)
