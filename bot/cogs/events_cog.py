from database.exceptions import ObjectNotFoundError
from database.managers import UserManager
from discord.ext import commands

import config


class EventsCog(commands.Cog):
    def __init__(self, bot):
        self._bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            UserManager.update(member.id, on_server=True)
        except ObjectNotFoundError:
            UserManager.create(member.id)

        role = member.guild.get_role(config.ON_JOIN_ROLE_ID)
        await member.add_roles(role)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            UserManager.update(member.id, on_server=False)
        except ObjectNotFoundError:
            UserManager.create(member.id, on_server=False)


def setup(bot):
    bot.add_cog(EventsCog(bot))
