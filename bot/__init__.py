from discord.ext import commands

import os

from .webhooks.log_hook import log


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.modules = []
        
    def launch(self, token):
        cogs_dir = os.path.join(os.path.curdir, 'bot', 'cogs')
        for filename in os.listdir(cogs_dir):
            if filename.endswith('_cog.py'):
                self.load_extension(f'bot.cogs.{filename[:-3]}')

        self.run(token)

    def load_module(self, module_name):
        modules_dir = os.path.join(os.path.curdir, 'bot', 'modules')
        module = module_name + '_module'
        for filename in os.listdir(modules_dir):
            if module == filename[:-3]:
                self.load_extension(f'bot.modules.{filename[:-3]}')
                self.modules.append(module_name)
                return

        raise ValueError(f'Module {module_name} is not found')

    def unload_module(self, module_name):
        modules_dir = os.path.join(os.path.curdir, 'bot', 'modules')
        module = module_name + '_module'
        for filename in os.listdir(modules_dir):
            if module == filename[:-3]:
                self.unload_extension(f'bot.modules.{filename[:-3]}')
                self.modules.remove(module_name)
                return

        raise ValueError(f'Module {module_name} is not found')

    async def on_ready(self):
        await log(f'Bot is logged in as {self.user.name}#{self.user.discriminator}')

    async def on_command_completion(self, ctx):
        author = f'{ctx.message.author.name}#{ctx.message.author.discriminator}'
        log_message = f'Command {ctx.command.name} invoked. Called in {ctx.channel.mention} by {author}'

        await log(log_message)
