"""
logout.py
@author Ryan Malacina
@SnoringNinja - https://snoring.ninja

Handles logging the bot out of discord
"""

from discord.ext import commands

from resources.config import ConfigLoader

class Logout():
    # pylint: disable=too-few-public-methods
    """
    Logout cog handles exiting discord and
    shutting down.
    """
    def __init__(self, bot):
        self.bot = bot
        self.owner_id = ConfigLoader().load_config_setting_int('BotSettings', 'owner_id')

    @commands.command(pass_context=True, no_pm=True)
    async def logout(self, ctx):
        """
        Logs the bot out.
        This can only be used by the bot owner.
        """
        user_id = ctx.message.author.id

        if int(user_id) == self.owner_id:
            await self.bot.say("Shutting down, bye!")
            await self.bot.logout()

        return

def setup(bot):
    """This makes it so we can actually use it."""
    bot.add_cog(Logout(bot))
