from itertools import repeat
from discord.ext import commands

import discord


class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command('clear')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=100, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel

        await ctx.message.delete()
        await channel.purge(limit=amount)

    @commands.command('kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, reason=None):
        await ctx.message.delete()
        await member.kick(reason=reason)

    @commands.command('ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, reason=None):
        await ctx.message.delete()
        await member.ban(reason=reason)

    @commands.command('say')
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx, channel: discord.TextChannel, *, text):
        await ctx.message.delete()
        await channel.send(text)


def setup(bot):
    bot.add_cog(ModerationCog(bot))
