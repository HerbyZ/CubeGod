from bot import Bot

import config

bot = Bot(command_prefix='!')
bot.launch(config.BOT_TOKEN)
