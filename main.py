import discord

from bot import Bot

import logging
import config

logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)

preloaded_modules = [
    'exchange_rates',
    'notification_roles'
]

bot = Bot(command_prefix='!', intents=discord.Intents.all(), preloaded_modules=preloaded_modules)


def main():
    bot.launch(config.BOT_TOKEN)


if __name__ == '__main__':
    main()
