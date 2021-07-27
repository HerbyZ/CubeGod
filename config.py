from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('DISCORD_BOT_API_TOKEN')

LOG_WEBHOOK_URL = os.getenv('LOG_WEBHOOK_URL')

DATABASE_CONNECTION_STRING = os.getenv('DATABASE_CONNECTION_STRING')

# Notification roles module
NOTIFICATION_ROLES_MESSAGE_ID = int(os.getenv('NOTIFICATION_ROLES_MESSAGE_ID'))

# Prison module
PRISONER_ROLE_ID = os.getenv('PRISONER_ROLE_ID')

# APIs
EXCHANGE_REST_API_KEY = os.getenv('EXCHANGE_REST_API_KEY')
