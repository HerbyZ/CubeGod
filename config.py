from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('DISCORD_BOT_API_TOKEN')

LOG_WEBHOOK_URL = os.getenv('LOG_WEBHOOK_URL')

DATABASE_CONNECTION_STRING = os.getenv('DATABASE_CONNECTION_STRING')
