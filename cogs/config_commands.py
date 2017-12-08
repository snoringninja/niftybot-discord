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

def contains_word(string, word):
    """Check if a word exists inside the string.

    @TODO: allow user to remove themselves from any of the configured
    groups that they are able to add themselves to

    @TODO: allow owners to add roles/channels simply by passing in the
    name of the role or channel instead of requiring them to use the
    snowflake ID; if there happens to be more than one of either, then
    require the owner to use the specific ID
    """
    return ' ' + word + ' ' in ' ' + string + ' '

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
    async def update_config(self, ctx, update_section: str, update_key: str, update_value: str): #pylint: disable=R0914
        """Update the configuration file

        :update_section: section to be updated in the config file
        :update_key: the key value to be updated in the passed in section
        :update_value: the value that matches the key
        """
        if update_section == 'ServerSettings':
            bot_message = await self.bot.say("This is a protected section.")
            await asyncio.sleep(5)
            await self.bot.delete_message(ctx.message)
            return await self.bot.delete_message(bot_message)
        else:
            try:
                member_id = ctx.message.author.id

                # This allows us to use #channel_name, @person_name
                update_value = update_value.replace('<@&', '')
                update_value = update_value.replace('<@!', '')
                update_value = update_value.replace('<#', '')
                update_value = update_value.replace('>', '')
                update_value = update_value.strip()

                bot_admin_users = []
                bot_admin_roles = []
                user_roles_list = []

                for user_role in ctx.message.author.roles:
                    user_roles_list.append(str(int(user_role.id)))

                try:
                    bot_admins_user_list = ConfigLoader().load_server_string_setting(
                        ctx.message.server.id,
                        'BotAdmins',
                        'bot_admin_users'
                    )

                    bot_admins_role_list = ConfigLoader().load_server_string_setting(
                        ctx.message.server.id,
                        'BotAdmins',
                        'bot_admin_roles'
                    )

                    for user in bot_admins_user_list.split():
                        bot_admin_users.append(user)

                    for role in bot_admins_role_list.split():
                        bot_admin_roles.append(role)
                except (configparser.NoSectionError, configparser.Error):
                    pass

                if update_section != 'BotAdmins':
                    if member_id == ctx.message.server.owner_id or \
                    int(member_id) == ConfigLoader().load_config_setting_int(
                            'BotSettings', 'owner_id'
                    ) or \
                    str(member_id) in bot_admin_users or \
                    [admin_role for admin_role in user_roles_list if admin_role in bot_admin_roles]:
                        filename = ctx.message.server.id
                        await self.update_config_file(
                            filename,
                            update_section,
                            update_key,
                            update_value,
                            ctx.message
                        )
                    else:
                        bot_message = await self.bot.say(
                            "Only the server owner can " \
                            "configure different plugins."
                        )
                        await asyncio.sleep(5)
                        await self.bot.delete_message(ctx.message)
                        return await self.bot.delete_message(bot_message)
                elif update_section == 'BotAdmins':
                    if member_id == ctx.message.server.owner_id or \
                    int(member_id) == ConfigLoader().load_config_setting_int(
                            'BotSettings', 'owner_id'
                    ):
                        await self.bot.say(
                            "Please use the botadmin command to update this section."
                        )
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

    @commands.command(pass_context=True, no_pm=False, name='botadmin')
    @commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
    async def update_role_list(self, ctx, add_or_remove: str, user_or_role: str, \
                               role_id: str):
        """Update the configured role list to add or remove
        a group.

        :user_or_role: (str) [user, role] passed in string to determine
        if it's a user or a role that is being updated

        :add_or_remove: (str) [add, remove] passed in string to determine
        if a role is being added or removed

        :role_id: the discord snowflake ID for the role, the pinged username
        :member: empty discord.Member object
        """
        member_id = ctx.message.author.id
        server_id = str(ctx.message.server.id)

        if member_id == ctx.message.server.owner_id or \
        int(member_id) == ConfigLoader().load_config_setting_int(
                'BotSettings', 'owner_id'
        ):
            if add_or_remove != 'add' and add_or_remove != 'remove':
                return await self.bot.say("Please specify if I am adding or removing a botadmin.")

            if user_or_role != 'user' and user_or_role != 'role':
                return await self.bot.say(
                    "Please specify if it's the user or role " \
                    "list I am updating."
                )

            current_id_list = ConfigLoader().load_server_string_setting(
                server_id,
                'BotAdmins',
                'bot_admin_users' if user_or_role == 'user' else 'bot_admin_roles'
            )

            # Hacky fix for when mentioning the role to strip stuff out
            role_id = role_id.replace('<@&', '')
            role_id = role_id.replace('<@!', '')
            role_id = role_id.replace('>', '')
            role_id = role_id.strip()

            if add_or_remove == 'add':
                if not contains_word(current_id_list, role_id):
                    if current_id_list == 'NOT_SET':
                        updated_id_list = role_id
                    else:
                        updated_id_list = current_id_list + " " + role_id
                else:
                    return await self.bot.say("Role already added.")

            if add_or_remove == 'remove':
                if contains_word(current_id_list, role_id):
                    updated_id_list = current_id_list.replace(role_id, '')

                if updated_id_list.isspace() or len(updated_id_list) == 0:
                    updated_id_list = 'NOT_SET'

            filename = ctx.message.server.id
            await ConfigCommands(self.bot).update_config_file(
                filename,
                'BotAdmins',
                'bot_admin_users' if user_or_role == 'user' else 'bot_admin_roles',
                updated_id_list.strip(),
                ctx.message
            )

def setup(bot):
    """This makes it so we can actually use it."""
    bot.add_cog(ConfigCommands(bot))
