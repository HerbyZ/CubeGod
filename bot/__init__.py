from discord.ext import commands

import os

from .webhooks import log_hook


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def launch(self, token):
        self.run(token)

    async def on_ready(self):
        await log_hook.execute(f'Bot is logged in as {self.user.name}#{self.user.discriminator}')

    async def on_message(self, message):
        if not message.author.bot:
            await message.channel.send(message.content)
