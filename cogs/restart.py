import discord
import asyncio
import random
import errno
import os
import sys
import traceback
import psutil

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

            await self.bot.say("Attempting restart...")
            await self.restart_process()
            await self.bot.say("...success?")
        else:
            print(userID)
            return

    async def restart_process(self):
        try:
            p = psutil.Process(os.getpid())
            for handler in p.get_open_files() + p.connections():
                os.close(handler.fd)
        except Exception as e:
            await error_logging().log_error(traceback.format_exc(), 'conn_reset_error')
            await self.bot.logou()
            sys.exit("Failed on restart.")

        python = sys.executable
        os.execl(python, python, *sys.argv)

        return

def setup(bot):
    """This makes it so we can actually use it."""
    bot.add_cog(Restart(bot))