"""
moderation.py
@author Ryan 'iBeNifty' Malacina
@site https://snoring.ninja

This is a collection of moderation based functions.
"""

import configparser
import asyncio

from resources.error import error_logging
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
        server_id = message.server.id
        try:
            plugin_enabled = ConfigLoader().load_server_config_setting_boolean(
                server_id,
                'Moderator',
                'enabled'
            )
            purge_everyone = ConfigLoader().load_server_config_setting_boolean(
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
            return await self.bot.say("Error with "
                                     )

        if plugin_enabled and purge_everyone:
            bot_message = await self.bot.say("{0.mention}: please refrain from using \
                                                everyone and and please use the here \
                                                highlight instead."
                                            )
            await self.bot.delete_message(message)
            await asyncio.sleep(5)
            return await self.bot.delete_message(bot_message)
