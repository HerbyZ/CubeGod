from discord.ext import commands

import discord

from database.models import User


class LevelSystemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith('!') or message.author.bot:
            return

        author_id = message.author.id

        try:
            user = User.find_one(author_id)
            new_exp = user.experience + 1
            new_level = user.level

            if new_exp >= 100:
                new_level += 1

            User.update(author_id, level=new_level, experience=new_exp)
        except ValueError:
            User.create(author_id)

    @commands.command('rank')
    async def get_rank(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.message.author

        user = User.find_one(member.id)
        # TODO: Create embed for !rank command
        await ctx.send(f'Юзер {member.nick}. Лвл - {user.level}, эксп - {user.experience}.')

    @commands.command('setlvl')
    @commands.has_permissions(kick_members=True)
    async def set_rank(self, ctx, member: discord.Member, level, exp=None):
        await ctx.message.delete()

        user = User.find_one(member.id)

        if exp is None:
            exp = user.experience

        User.update(user.discord_id, level=level, experience=exp)


def setup(bot):
    bot.add_cog(LevelSystemCog(bot))
