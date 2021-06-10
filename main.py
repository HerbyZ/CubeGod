from bot import Bot

import logging
import config

logging.basicConfig(
    format='%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO
)

bot = Bot(command_prefix='!')
bot.launch(config.BOT_TOKEN)
