from discord.ext import commands
from discord import utils


class NotificationRolesModule(commands.Cog):
    def __init__(self, bot):
        self._bot = bot

        # Change to your emojis and role ids
        self._roles = {
            '❤️': 731862587683242064,
            '🎮': 731876639255822386,
            '🍩': 731877205306507274
        }

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message_id = payload.message_id
        if message_id != 731877822930354268:
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
        if message_id != 731877822930354268:
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
