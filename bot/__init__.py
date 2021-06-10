from discord.ext import commands

import os

from .webhooks import log_hook


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def launch(self, token):
        self.run(token)

    async def on_ready(self):
        await log_hook.log(f'Bot is logged in as {self.user.name}#{self.user.discriminator}')

    async def on_command_completion(self, ctx):
        author = f'{ctx.message.author.name}#{ctx.message.author.discriminator}'
        log_message = f'Command {ctx.command.name} was used in {ctx.channel.mention} by {author}'

        await log_hook.log(log_message)
