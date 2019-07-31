# -*- coding: utf-8 -*-
import os
import sys

from discord.ext import commands
from resources.config import ConfigLoader

class Restart:
    """
    Restart the bot python process
    I wouldn't recommend using this in its current state, as it's fairly buggy and may not always work right
    """
    def __init__(self, bot):
        self.bot = bot
        self.owner_id = ConfigLoader().load_config_setting_int('BotSettings', 'owner_id')

    @commands.command(pass_context=True, no_pm=True)
    async def restart(self, ctx):
        """Handles calling the restart process
        if invoked by the bot owner
        """
        user_id = ctx.message.author.id

        if int(user_id) == self.owner_id:

            await self.bot.say("Restarting!")
            await self.bot.logout()
            await self.restart_process()

    async def restart_process(self):
        """

        :return:
        """
        os.execv(sys.executable, ['python'] + sys.argv)

def setup(bot):
    """This makes it so we can actually use it."""
    bot.add_cog(Restart(bot))
