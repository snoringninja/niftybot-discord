import discord
import asyncio
import random
import errno
import os
import sys
import traceback

from discord.ext import commands

from resources.error import error_logging
from resources.config import ConfigLoader
from resources.general_resources import BotResources

class Restart():
    def __init__(self, bot):
        self.bot = bot
        self.owner_id = ConfigLoader().load_config_setting_int('BotSettings', 'owner_id')

    @commands.command(pass_context=True, no_pm=True)
    async def restart(self, ctx, member: discord.Member = None):
        userID = ctx.message.author.id

        if int(userID) == self.owner_id:

            await self.bot.say("Restarting!")
            await self.bot.logout()
            await self.restart_process()

    async def restart_process(self):
        os.execv(sys.executable, ['python'] + sys.argv)

def setup(bot):
    """This makes it so we can actually use it."""
    bot.add_cog(Restart(bot))
