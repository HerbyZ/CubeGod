from discord.ext import commands

from bot.webhooks.log_hook import log


class ModulesCog(commands.Cog):
    def __init__(self, bot):
        self._bot = bot

    @commands.command('load-module')
    @commands.has_permissions(manage_guild=True)
    async def _load_module_command(self, ctx, module_name):
        author = ctx.message.author

        if module_name in self._bot.modules:
            await author.send(f'Module {module_name} is already loaded')

        try:
            self._bot.load_module(module_name)
        except ValueError:
            return await author.send(f'Module {module_name} is not found.')

        await ctx.message.add_reaction('✅')

        await log(f'User {author.name}#{author.discriminator} loaded module {module_name}')

    @commands.command('unload-module')
    @commands.has_permissions(manage_guild=True)
    async def _unload_module_command(self, ctx, module_name):
        author = ctx.message.author

        if module_name not in self._bot.modules:
            await author.send(f'Module {module_name} is not loaded.')

        try:
            self._bot.unload_module(module_name)
        except ValueError:
            return await author.send(f'Module {module_name} is not found.')

        await ctx.message.add_reaction('✅')

        await log(f'User {author.name}#{author.discriminator} unloaded module {module_name}')

    @commands.command('reload-module')
    @commands.has_permissions(manage_guild=True)
    async def _reload_module_command(self, ctx, module_name):
        author = ctx.message.author

        if module_name not in self._bot.modules:
            await author.send(f'Module {module_name} is not loaded.')

        try:
            self._bot.unload_module(module_name)
            self._bot.load_module(module_name)
        except ValueError:
            return await author.send(f'Module {module_name} is not found.')

        await ctx.message.add_reaction('✅')

        await log(f'User {author.name}#{author.discriminator} reloaded module {module_name}')

    @commands.command('loaded-modules')
    @commands.has_permissions(manage_guild=True)
    async def _get_loaded_modules(self, ctx):
        author = ctx.message.author
        modules = ''.join(f'{module}, ' for module in self._bot.modules)[:-2]  # Sorry for this

        await ctx.message.delete()
        await author.send(f'Loaded modules: {modules}.')
        await log(f'User {author.name}#{author.discriminator} requested loaded modules list')


def setup(bot):
    bot.add_cog(ModulesCog(bot))
