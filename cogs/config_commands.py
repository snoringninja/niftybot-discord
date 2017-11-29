"""
generate_config.py
@author xNifty
@site https://snoring.ninja

Handles all configuration based commands
"""

import os
import configparser
import asyncio

import discord
from discord.ext import commands
from resources.config import ConfigLoader

def load_config(default_filename):
    """Load the config file.
    :default_filename: name of the config file to load
    """
    config = configparser.ConfigParser()
    return config.read(default_filename)

class ConfigCommands():
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

        if member_id == ctx.message.server.owner_id or \
        int(member_id) == ConfigLoader().load_config_setting_int('BotSettings', 'owner_id'):
            file_exists = await ConfigLoader(self.bot).check_if_config_exists(
                ctx.message.server.id
            )

            if not file_exists:
                await ConfigLoader(self.bot).generate_default_config_file(
                    ctx.message.server.id,
                    member_id
                )
            else:
                await self.bot.say("Configuration file already exists.")
        else:
            return

    async def update_config_file(self, filename, update_section, \
                                 update_key, update_value, message, supress_message=False
                                ): #pylint: disable=too-many-arguments
        """Handle updating the config file for the server.
        supress_message is used when we update the config from a function when a command fails
        It defaults to False for when the config is updating from within the server
        """
        parser = configparser.ConfigParser()
        loaded_file = load_config(
            '%s.ini' % (
                os.path.join(
                    self.server_settings_path,
                    str(filename)
                )
            ),
        )
        parser.read(loaded_file)

        if parser.has_section(update_section):
            if parser.has_option(update_section, update_key):
                parser.set(update_section, update_key, update_value)

                with open(
                    '%s.ini' % (
                        os.path.join(
                            self.server_settings_path,
                            str(filename)
                        )
                    ), 'w') as configfile:
                    parser.write(configfile)
                if not supress_message:
                    bot_message = await self.bot.say("Configuration file updated.")
                    await asyncio.sleep(5)
                    await self.bot.delete_message(message)
                    return await self.bot.delete_message(bot_message)
                else:
                    return
            else:
                return await self.bot.say("Key '{0}' does not exist.".format(update_key))
        else:
            return await self.bot.say("Section '{0}' does not exist.".format(update_section))

    @commands.command(pass_context=True, no_pm=True, name='config')
    @commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
    async def update_config(self, ctx, update_section: str, update_key: str, update_value: str):
        """Update the configuration file

        :update_section: section to be updated in the config file
        :update_key: the key value to be updated in the passed in section
        :update_value: the value that matches the key
        """
        if update_section == 'ServerSettings':
            return await self.bot.say("This is a protected section.")
        else:
            try:
                member_id = ctx.message.author.id

                bot_admin_users = []
                bot_admin_roles = []

                try:
                    bot_admins_user_list = ConfigLoader().load_server_config_setting(ctx.message.server.id, 'ServerSettings', 'bot_admin_users')
                    for plugin in bot_admins_user_list.split():
                        bot_admin_users.append(plugin)
                except:
                    pass

                if member_id == ctx.message.server.owner_id or \
                int(member_id) == ConfigLoader().load_config_setting_int('BotSettings', 'owner_id') or \
                str(member_id) in bot_admin_users:
                    filename = ctx.message.server.id
                    await self.update_config_file(
                        filename,
                        update_section,
                        update_key,
                        update_value,
                        ctx.message
                    )
                else:
                    return await self.bot.say("Only the server owner can configure different plugins.")
            except (configparser.NoSectionError, configparser.NoOptionError) as config_error:
                print("Error with updating the configuration file: \n{0}".format(config_error))

    @commands.command(pass_context=True, no_pm=True, name='getconfig')
    @commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
    async def get_config_information(self, ctx, member: discord.Member=None):
        """Get the server configuration settings and send in a private message

        :member: empty discord.Member object
        """
        member = ctx.message.author
        member_id = ctx.message.author.id
        server_id = ctx.message.server.id

        try:
            if member_id == ctx.message.server.owner_id or \
            int(member_id) == ConfigLoader().load_config_setting_int('BotSettings', 'owner_id'):
                return_string = "```Settings for {0}:\n\n".format(ctx.message.server.name)

                parser = configparser.ConfigParser()
                loaded_file = load_config(
                    '%s.ini' % (
                        os.path.join(
                            self.server_settings_path,
                            str(server_id)
                        )
                    ),
                )
                parser.read(loaded_file)

                for section in parser.sections():
                    return_string = return_string + section + ":\n"
                    for name, value in parser.items(section):
                        return_string = return_string + "{0}: {1}".format(name, value) + "\n"
                        return_string = return_string + "\n"

                return_string = return_string + "```"

                await self.bot.send_message(member, return_string)
                return await self.bot.delete_message(ctx.message)
        except discord.Forbidden:
            bot_message = await self.bot.say(
                "I am unable to message you. You may have me blocked, " \
                "or personal messages disabled."
            )
            await asyncio.sleep(5)
            await self.bot.delete_message(ctx.message)
            return await self.bot.delete_message(bot_message)
        except configparser.Error as config_error:
            print("Error with the configuration file: \n{0}".format(config_error))

def setup(bot):
    """This makes it so we can actually use it."""
    bot.add_cog(ConfigCommands(bot))
