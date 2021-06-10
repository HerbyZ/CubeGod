from discord.ext import commands

import os

from .webhooks import log_hook


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def launch(self, token):
        cogs_dir = os.path.join(os.path.curdir, 'bot', 'cogs')
        for filename in os.listdir(cogs_dir):
            if filename.endswith('_cog.py'):
                self.load_extension(f'bot.cogs.{filename[:-3]}')

        self.run(token)

    async def on_ready(self):
        await log_hook.log(f'Bot is logged in as {self.user.name}#{self.user.discriminator}')

    async def on_command_completion(self, ctx):
        author = f'{ctx.message.author.name}#{ctx.message.author.discriminator}'
        log_message = f'Command {ctx.command.name} was used in {ctx.channel.mention} by {author}'

        await log_hook.log(log_message)
