from dotenv import load_dotenv

import os
import pytz

load_dotenv()


BASE_DIR = os.path.abspath(os.path.curdir)

TIMEZONE = pytz.timezone('Europe/Moscow')  # Moscow time UTC+3:00

# Discord

BOT_TOKEN = os.getenv('DISCORD_BOT_API_TOKEN')

LOG_WEBHOOK_URL = os.getenv('LOG_WEBHOOK_URL')

ON_JOIN_ROLE_ID = int(os.getenv('ON_JOIN_ROLE_ID'))


# Bot modules

NOTIFICATION_ROLES_MESSAGE_ID = int(os.getenv('NOTIFICATION_ROLES_MESSAGE_ID'))

PRISONER_ROLE_ID = os.getenv('PRISONER_ROLE_ID')

EXCHANGE_RATES_WEBHOOK_URL = os.getenv('EXCHANGE_RATES_WEBHOOK_URL')


# Database

DATABASE_CONNECTION_STRING = os.getenv('DATABASE_CONNECTION_STRING')

# APIs

EXCHANGE_REST_API_KEY = os.getenv('EXCHANGE_REST_API_KEY')
