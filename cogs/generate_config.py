"""
generate_config.py
@author Ryan 'iBeNifty' Malacina
@site https://snoring.ninja

Calls the function in config_updater.py to create a config file
for a server
"""

import traceback
import os

from discord.ext import commands
from resources.error import error_logging
from resources.config import ConfigGenerator
from resources.config import ConfigLoader

class GenerateConfig():
    """GenerateConfig controls the generate_config command"""
    def __init__(self, bot):
        self.bot = bot
        self.server_settings_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         '../channel_settings')
        )

    @commands.command(pass_context=True, no_pm=True, name='genconfig')
    @commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
    async def generate_config(self, ctx):
        """
        Checks if the member is the server or the
        bot owner and if so runs the generate_config function
        from the general_bot_resources
        """
        member_id = ctx.message.author.id

        try:
            if member_id == ctx.message.server.owner_id or \
            int(member_id) == ConfigLoader().load_config_setting_int('BotSettings', 'owner_id'):
                file_exists = await ConfigGenerator(self.bot).checkIfConfigExists(
                    ctx.message.server.id
                )

                if not file_exists:
                    await ConfigGenerator(self.bot).generateDefaultConfigFile(
                        ctx.message.server.id,
                        member_id
                    )
                else:
                    await self.bot.say("Configuration file already exists.")
            else:
                return
        except Exception:
            await error_logging().log_error(
                traceback.format_exc(),
                'GenerateConfig: generateConfig'
            )

def setup(bot):
    """This makes it so we can actually use it."""
    bot.add_cog(GenerateConfig(bot))
