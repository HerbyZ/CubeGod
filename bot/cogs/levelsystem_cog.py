from bot.webhooks.log_hook import log
from discord.ext import commands

import discord

from database.managers import UserManager


class LevelSystemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith('!') or message.author.bot:
            return

        author_id = message.author.id

        try:
            user = UserManager.find_one(author_id)
            new_exp = user.experience + 1
            new_level = user.level

            if new_exp >= 100:
                new_level += 1
                new_exp = 0

            user.update(level=new_level, experience=new_exp)
        except ValueError:
            UserManager.create(author_id)

    @commands.command('rank')
    async def get_rank(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.message.author

        try:
            user = UserManager.find_one(member.id)
            # TODO: Create embed for !rank command
            await ctx.send(f'**Юзер {member.name}. Лвл - {user.level}, эксп - {user.experience}.**')
        except ValueError:
            await ctx.send(f'**Юзер не найден :(**')

    @commands.command('setlvl')
    @commands.has_permissions(kick_members=True)
    async def set_rank(self, ctx, member: discord.Member, level, exp=None):
        await ctx.message.delete()

        user = UserManager.find_one(member.id)

        if exp is None:
            exp = user.experience

        UserManager.update(user.discord_id, level=level, experience=exp)

        author = f'{ctx.message.author.name}#{ctx.message.author.discriminator}'
        await log(f'Command !setlvl was used by {author} on {member.nick} with level {level} exp {exp}')


def setup(bot):
    bot.add_cog(LevelSystemCog(bot))
