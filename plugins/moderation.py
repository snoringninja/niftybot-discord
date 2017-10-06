"""
moderation.py
@author Ryan 'iBeNifty' Malacina
@site https://snoring.ninja

This is a collection of moderation based functions.
"""

import configparser
import traceback
import asyncio
import discord

from resources.error import ErrorLogging
from resources.config import ConfigLoader
from cogs.config_updater import ConfigUpdater

class Moderation():
    """Collection of moderator plugins."""
    def __init__(self, bot):
        self.bot = bot

    async def purge_everyone_message(self, message):
        """
        If the server owner has configured this, then when someone
        who is not in the approved userID list tries to use
        @everyone the bot will delete the message and tell them
        to please use @here instead
        """
        try:
            server_id = message.server.id
            channel_id = message.channel.id
            member = message.author
            try:
                plugin_enabled = ConfigLoader().load_server_boolean_setting(
                    server_id,
                    'Moderator',
                    'enabled'
                )
                purge_everyone = ConfigLoader().load_server_boolean_setting(
                    server_id,
                    "Moderator",
                    "purge_everyone"
                )
            except configparser.NoSectionError:
                await ConfigUpdater(self.bot).updateConfigFile(
                    server_id,
                    'Moderator',
                    'enabled',
                    'False',
                    True
                )
                print("No section existed for Moderator.")
                return

            if plugin_enabled and purge_everyone:
                bot_message = await self.bot.send_message(discord.Object(id=channel_id),
                                                          "{0.mention}: please refrain from using \
                                                          [@]everyone and and please use \
                                                          the [@]here highlight instead."
                                                          .format(member)
                                                         )
                await self.bot.delete_message(message)
                await asyncio.sleep(5)
                return await self.bot.delete_message(bot_message)
        except:
            await ErrorLogging().log_error(
                traceback.format_exc(),
                'Moderation: purge_everyone_message'
            )
