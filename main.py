# -*- coding: utf-8 -*-
"""
main.py
@author Ryan Malacina
@SnoringNinja - https://snoring.ninja

Built on discord.py
"""

import asyncio
import sys
import traceback

# Import the plugins folder
# @TODO : config to enable / disable plugin files to be imported
from plugins.moderation import Moderation
from plugins.join_leave_handler import JoinLeaveHandler

from resources.error_logger import ErrorLogging

from resources.config import ConfigLoader
from resources.general_resources import BotResources

import discord
from discord.ext.commands.view import StringView
from discord.ext import commands

BOT_CONFIG_GENERATED = ConfigLoader().check_for_bot_config()
if not BOT_CONFIG_GENERATED:
    print("Please configure the newly generated niftybot.ini file before restarting the bot.")
    raise SystemExit

# Not sure we still need this
DESCRIPTION = ConfigLoader().load_config_setting('BotSettings', 'description')

# Load the command prefix from the core ini
COMMAND_PREFIX = ConfigLoader().load_config_setting('BotSettings', 'command_prefix')

# Load the bot token from the core ini
BOT_TOKEN = ConfigLoader().load_config_setting('BotSettings', 'bot_token')

# Set the game name from the core ini
GAME_NAME = ConfigLoader().load_config_setting('BotSettings', 'game_name')

# load the database name from the core ini
DATABASE_NAME = ConfigLoader().load_config_setting('BotSettings', 'sqlite')

# Create the plugin list, which is built from the core ini file
EXTENSIONS = ConfigLoader().load_config_setting('BotSettings', 'enabled_plugins')

NOT_ACCEPTED_MESSAGE = ConfigLoader().load_config_setting_string(
    'BotSettings',
    'not_accepted_message'
)

SHOW_DEBUG = str(
    ConfigLoader().load_config_setting_boolean('Debugging', 'error_handle_debugger')
)

CLIENT = commands.Bot(command_prefix=COMMAND_PREFIX, description=DESCRIPTION)

@CLIENT.event
async def on_message(message):
    """
    discord.py on_message
    processes messages and checks if a command
    """
    view = StringView(message.content)
    invoked_prefix = COMMAND_PREFIX

    invoked_prefix = discord.utils.find(view.skip_string, COMMAND_PREFIX)
    discord.utils.find(view.skip_string, COMMAND_PREFIX)

    if "@everyone" in message.content:
        await Moderation(CLIENT).purge_everyone_message(message)

    if invoked_prefix is None:
        return

    invoker = view.get_word()

    #print(invoker)
    #print(CLIENT.commands)

    if invoker in CLIENT.commands:
        # @TODO : bot config update for override commands to make this cleaner
        if message.content == '{0}accept'.format(COMMAND_PREFIX):
            await CLIENT.process_commands(message)
        elif message.content.startswith("{0}guild".format(COMMAND_PREFIX)):
            await CLIENT.process_commands(message)
        elif message.content.startswith("{0}genconfig".format(COMMAND_PREFIX)):
            await CLIENT.process_commands(message)
        else:
            can_use = BotResources().check_accepted(message.author.id)
            message_channel_valid = BotResources().get_tos_channel_valid(message.server.id)
            if can_use:
                await CLIENT.process_commands(message)
            elif not can_use and message_channel_valid:
                if message.author.id != CLIENT.user.id:
                    message_channel_id = ConfigLoader().load_server_int_setting(
                        message.server.id,
                        'ConfigSettings',
                        'not_accepted_channel_id'
                    )

                    bot_message = await CLIENT.send_message(
                        discord.Object(id=message_channel_id),
                        NOT_ACCEPTED_MESSAGE.format(
                            message.author,
                            COMMAND_PREFIX
                        )
                    )
                    await asyncio.sleep(20)
                    await CLIENT.delete_message(bot_message)
            else:
                # This is needed to prevent infinite looping message posting
                if message.author.id != CLIENT.user.id:
                    bot_message = await CLIENT.send_message(
                        discord.Object(id=message.channel.id),
                        NOT_ACCEPTED_MESSAGE.format(
                            message.author,
                            COMMAND_PREFIX
                        )
                    )
                    await asyncio.sleep(20)
                    await CLIENT.delete_message(bot_message)

@CLIENT.event
async def on_ready():
    """
    discord.py on_ready
    """
    print('------')
    print('Logged in as {0}; CLIENT ID: {1}'.format(str(CLIENT.user.name), str(CLIENT.user.id)))
    print('Command prefix is: {0}'.format(str(COMMAND_PREFIX)))
    print('Setting game to: {0}'.format(GAME_NAME))
    print('Loaded extensions: {0}'.format(EXTENSIONS))
    print('Database name: {0}'.format(DATABASE_NAME))
    await CLIENT.change_presence(game=discord.Game(type=0, name=GAME_NAME))
    print('Good to go!')
    print('------')

@CLIENT.event
async def on_member_join(member):
    """
    discord.py on_member_join

    when a member joins a server, check if the server has a channel configured
    and if they have the member_join_enabled plugin enabled
    """
    server = member.server
    await JoinLeaveHandler(CLIENT).welcome_user(server.id, member, server)

@CLIENT.event
async def on_member_remove(member):
    """
    discord.py on_member_remove

    when a member leaves a server, check if the server has a channel configured
    and if they have the member_part_enabled plugin enabled
    """
    server = member.server
    await JoinLeaveHandler(CLIENT).goodbye_user(server.id, member)

@CLIENT.event
async def on_command_error(exception, context):
    """
    Override the default discord.py on_command_error
    to log our errors to a file in the errors
    folder.

    @TODO : better error logging
    """

    if hasattr(context.command, "on_error"):
        print('Ignoring exception in command {}'.format(context.command), file=sys.stderr)
        return

    if isinstance(exception, commands.CommandNotFound):
        print('Ignoring exception in command {}'.format(context.command), file=sys.stderr)
        return

    if isinstance(exception, commands.DisabledCommand):
        print('Ignoring exception in command {}'.format(context.command), file=sys.stderr)
        return

    if isinstance(exception, commands.NoPrivateMessage):
        print('Ignoring exception in command {}'.format(context.command), file=sys.stderr)
        return

    if isinstance(exception, commands.MissingRequiredArgument):
        print('Ignoring exception in command {}'.format(context.command), file=sys.stderr)
        return

    if SHOW_DEBUG:
        traceback.print_exception(
            type(exception),
            exception,
            exception.__traceback__,
            file=sys.stderr
        )

    print("Generating an error log from command {0}".format(context.command), file=sys.stderr)
    await ErrorLogging().log_error(
        traceback.format_exception(
            type(exception),
            exception,
            exception.__traceback__
        ),
        context.command
    )

def main():
    """
    main section of the bot

    """
    print('Preparing...')
    ErrorLogging().create_directory()
    ConfigLoader().create_directory()
    try:
        startup_extensions = []
        for plugin in EXTENSIONS.split():
            startup_extensions.append(plugin)

        CLIENT.remove_command("help")

        for extension in startup_extensions:
            try:
                CLIENT.load_extension(extension)
            except (ValueError, AttributeError, TypeError, ImportError) as err:
                exc = '{}: {}'.format(type(err).__name__, err)
                print('Failed to load extension {}\n{}\n'.format(extension, exc))
        CLIENT.run(BOT_TOKEN)
    except AttributeError:
        CLIENT.logout()
        raise AttributeError
    except TypeError:
        CLIENT.logout()
        raise TypeError
    except discord.LoginFailure as login_error:
        print("There was an issue with logging in:\n{0}\n".format(login_error))
        raise SystemExit

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        print("Bot process was terminated by a SystemExit.")
        sys.exit(0)
    except AttributeError:
        print("Bot process was terminated by an AttributeError.")
        sys.exit(0)
    except TypeError:
        print("Bot process was terminated by an TypeError.")
        sys.exit(0)
