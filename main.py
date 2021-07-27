from bot import Bot

import config
import database
import discord
import logging

logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)

preloaded_modules = []

bot = Bot(command_prefix='!', intents=discord.Intents.all(), preloaded_modules=preloaded_modules)


def main():
    database.init()
    bot.launch(config.BOT_TOKEN)


if __name__ == '__main__':
    main()
