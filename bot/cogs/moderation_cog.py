from database.exceptions import ObjectNotFoundError
from database.managers import UserManager
from discord.ext import commands

import discord

from ..webhooks.log_hook import log


class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self._bot = bot

    @commands.command('clear')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=100, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel

        await ctx.message.delete()
        await channel.purge(limit=amount)
        
        author = f'{ctx.message.author.name}#{ctx.message.author.discriminator}'
        await log(f'Command !clear was used in channel {channel} by user {author} with amount {amount}')

    @commands.command('kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await ctx.message.delete()
        await member.kick(reason=reason)

        author = f'{ctx.message.author.name}#{ctx.message.author.discriminator}'
        await log(f'Command !kick was used by {author} on user {member.nick}')

    @commands.command('ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        author = ctx.message.author
        author_name = f'{author.name}#{author.discriminator}'
        member_name = f'{member.name}#{member.discriminator}'
        await ctx.message.delete()

        # Ban user in db
        try:
            user = UserManager.find_one(member.id)
        except ObjectNotFoundError:
            user = UserManager.create(member.id)

        if not user.is_banned:
            user.ban(reason)
        else:
            await author.send(f'User {member_name} is already banned (in database).')

        # Ban user on server
        await member.ban(reason=reason)

        await log(f'Command !ban was used by {author_name} on user {member_name}')

    @commands.command('unban')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id):
        author = ctx.message.author

        await ctx.message.delete()

        try:
            int(user_id)
        except ValueError:
            return await author.send('You should use user\'s id instead of his name')

        try:
            user = UserManager.find_one(user_id)
            if not user.is_banned:
                return await author.send(f'User is not banned.')

            user.unban()
        except ObjectNotFoundError:
            await author.send(f'User not found in database, trying to unban on server...')

        user = await self._bot.fetch_user(user_id)
        guild = ctx.guild

        try:
            await guild.fetch_ban(user)
            await guild.unban(user)
        except discord.NotFound:
            await author.send('User is not banned')

    @commands.command('getbans')
    @commands.has_permissions(ban_members=True)
    async def get_bans(self, ctx, user_id):
        author = ctx.message.author

        try:
            int(user_id)
        except ValueError:
            return await author.send('You should use user\'s id instead of his name')

        try:
            user = UserManager.find_one(user_id)
        except ObjectNotFoundError:
            return await author.send(f'User with id {user_id} not found.')

        bans = user.get_bans()
        if len(bans) == 0:
            return await author.send(f'User with id {user_id} has no bans.')

        bans_str = ''
        for ban in bans:
            bans_str += f'**Date**: {ban.date}; **Is active**: {ban.is_active}; ' \
                        f'**Id**: {ban.id}; **Reason**: {ban.reason}.\n'

        await author.send(f'Bans list for user with id {user_id}\n' + bans_str)
        await log(f'User {author.name}#{author.discriminator} requested bans history for user with id {user_id}.')

    @commands.command('say')
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx, channel: discord.TextChannel, *, text):
        await ctx.message.delete()
        await channel.send(text)

        author = f'{ctx.message.author.name}#{ctx.message.author.discriminator}'
        await log(f'Command !say was used in channel {channel} by user {author} with text:\n```{text}```')


def setup(bot):
    bot.add_cog(ModerationCog(bot))
