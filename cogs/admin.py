from discord.ext import commands
from cogs.utils import checks
import discord
import inspect
import traceback

# to expose to the eval command
import datetime
from collections import Counter

import importlib

class Admin:
    """Admin-only commands that make the bot dynamic."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @checks.is_owner()
    async def load(self, *, module : str):
        """Loads a module."""
        try:
            self.bot.load_extension(module)
        except Exception as e:
            await self.bot.say('\N{PISTOL}')
            await self.bot.say('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.say('\N{OK HAND SIGN}')

    @commands.command(hidden=True)
    @checks.is_owner()
    async def unload(self, *, module : str):
        """Unloads a module."""
        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await self.bot.say('\N{PISTOL}')
            await self.bot.say('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.say('\N{OK HAND SIGN}')

    @commands.command(name='reload', hidden=True)
    @checks.is_owner()
    async def _reload(self, *, module : str):
        """Reloads a module."""
        try:
            print("Unloading...")
            self.bot.unload_extension(module)
            print("Attempting reload...")
            self.bot.load_extension(module)
        except Exception as e:
            await self.bot.say("{0}".format(traceback.format_exc()))
        else:
            await self.bot.say('\N{OK HAND SIGN}')

def setup(bot):
    bot.add_cog(Admin(bot))