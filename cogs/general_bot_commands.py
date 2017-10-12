"""
general_bot_commands.py
@author Ryan 'iBeNifty' Malacina
@site https://snoring.ninja

Class to handle general bot commands that have no
place in other classes.
"""

import traceback
import asyncio

import discord
from discord.ext import commands

from resources.database import DatabaseHandler
from resources.config import ConfigLoader
from resources.error import ErrorLogging
from resources.general_resources import BotResources
from resources.decorators import error_logger

class BotCommands:
    """
    Class to control multiple different functions that
    have no place in other classes.
    """
    def __init__(self, bot):
        self.bot = bot
        self.prefix = ConfigLoader().load_config_setting('BotSettings', 'command_prefix')

    @commands.command(pass_context=True, no_pm=False, name='accept')
    @commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
    async def add_accepted_user(self, ctx, member: discord.Member=None):
        """
        If a user accepts the bot terms of service, and has not
        already accepted the terms of service, this will enter them
        into the database so they won't need to accept the terms again.
        """
        member = ctx.message.author
        member_id = ctx.message.author.id

        try:
            print("Member ID: {0}".format(member_id))
            has_accepted = BotResources().check_accepted(member_id)
            print(has_accepted)
            if has_accepted:
                return await self.bot.say("You've already accepted my terms of service.")
            else:
                try:
                    query = """INSERT INTO accepted_users (discord_id) VALUES (?)"""
                    DatabaseHandler().insert_into_database(query, (str(member_id), ))
                    return await self.bot.say("{0.mention}: thanks for accepting. You may now \
                                                use commands.".format(member))
                except Exception:
                    await ErrorLogging().log_error(
                        traceback.format_exc(),
                        'BotCommands: add_accepted_user'
                    )
        except Exception:
            await ErrorLogging().log_error(
                traceback.format_exc(),
                'BotCommands: add_accepted_user'
            )

    @commands.command(pass_context=True, no_pm=True, name='nick')
    @commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
    async def change_username(self, ctx, username: str):
        """
        Change the bot username.
        """
        member_id = ctx.message.author.id

        try:
            if (member_id == ctx.message.server.owner_id
                    or int(member_id) == ConfigLoader().load_config_setting_int(
                        'BotSettings',
                        'owner_id'
                    )
               ):
                await self.bot.change_nickname(ctx.message.server.me, username)
                return await self.bot.say("Changed my username!")
        except Exception:
            await ErrorLogging().log_error(traceback.format_exc(), 'BotCommands: change_username')

    @commands.command(pass_context=True, no_pm=True, name="help")
    @commands.cooldown(rate=1, per=30, type=commands.BucketType.server)
    async def get_help(self, ctx, member: discord.Member=None):
        """
        Return the link for the bot documentation.
        """
        member = ctx.message.author
        return await self.bot.say("{0.mention}: Please see https://xnifty.github.io \
                                    for now.".format(member))

def setup(bot):
    """This makes it so we can actually use it."""
    bot.add_cog(BotCommands(bot))
