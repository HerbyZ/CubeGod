from discord.ext import commands
from discord import utils

import config


class NotificationRolesModule(commands.Cog):
    def __init__(self, bot):
        self._bot = bot

        # Change to your emojis and role ids
        self._roles = {
            '❤️': 868532368569421845,
            '🎮': 868532411930132520,
            '🍩': 868532440799526922
        }
        # Change to your message id
        self._message_id = config.NOTIFICATION_ROLES_MESSAGE_ID

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message_id = payload.message_id
        if message_id != self._message_id:
            return

        channel = self._bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(message_id)
        member = utils.get(message.guild.members, id=payload.user_id)

        try:
            emoji = str(payload.emoji)
            role = utils.get(message.guild.roles, id=self._roles[emoji])

            if role not in member.roles:
                await member.add_roles(role)
            else:
                await message.remove_reaction(payload.emoji, member)
        except KeyError:
            return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        message_id = payload.message_id
        if message_id != self._message_id:
            return

        channel = self._bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(message_id)
        member = utils.get(message.guild.members, id=payload.user_id)

        try:
            emoji = str(payload.emoji)
            role = utils.get(message.guild.roles, id=self._roles[emoji])

            await member.remove_roles(role)
        except KeyError:
            return


def setup(bot):
    bot.add_cog(NotificationRolesModule(bot))
