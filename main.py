# -*- coding: utf-8 -*-

# main.py
# @author Ryan Malacina
# @SnoringNinja - https://snoring.ninja
# Built on discord.py
# Above files not included
# 

# TODO : clean up everything, and by that I mean organize plugins into
#        their own folder and import based on that...possibly just write something to import them all
#        at once based on a config file

import discord
import asyncio
#import spotilib

# Import the plugins folder
# TODO : config to enable / disable plugin files to be imported
import plugins

# Import the commands folder
# TODO : config to enable / disable command files to be imported
import commands

# this needs to be cleaned up
from resources import database
from resources.error import error_logging

from discord.ext import commands

import os
import sys

from commands.utils import checks

from resources.config import ConfigLoader

# TODO : this is just...well, ugly
description = ConfigLoader().load_config_setting('botsettings', 'description')
command_prefix = ConfigLoader().load_config_setting('botsettings', 'command_prefix')
bot_token = ConfigLoader().load_config_setting('botsettings', 'bot_token')
game_name = ConfigLoader().load_config_setting('botsettings', 'game_name')
show_db_info = ConfigLoader().load_config_setting('debugging', 'show_db_info')

# TODO : Get listed plugins from settings; not listed = don't use
extension_list = ConfigLoader().load_config_setting('botsettings', 'enabled_plugins')

client = commands.Bot(command_prefix=command_prefix, description=description)

@client.event
async def on_message(message):
    server = message.server
    gen = server.emojis

    for x in gen:
        print(x)
    await client.process_commands(message)

@client.event
async def on_ready():
    print('------')
    print('Logged in as {0}; Client ID: {1}'.format(str(client.user.name), str(client.user.id)))
    print('Command prefix is: {0}'.format(str(command_prefix)))
    print('Setting game to: {0}'.format(game_name))
    print('Loaded extensions: {0}'.format(extension_list))
    await client.change_presence(game=discord.Game(name=game_name))
    print('------')

@client.event
async def on_member_join(member):
    server = member.server
    fmt = 'Welcome to {0.name}\'s Discord, {1.mention}! Relax and have some fun! <:uni:311535311555395584>'
    await client.send_message(server, fmt.format(server, member))

if __name__ == "__main__":
    # attempt to connect to the database first before trying anything else
    # try catch for obvious reasons
    print('------')
    print('Checking database before continuing...')
    database.DatabaseHandler().get_conn_details() if show_db_info == True else False
    error_logging().create_directory()
    try:
        database.DatabaseHandler().attemptConnection()
        print('Connection successful.')

        gen = client.get_all_emojis()
        for x in gen:
            print(x)

        startup_extensions = []
        for plugin in extension_list.split():
            startup_extensions.append(plugin)

        for extension in startup_extensions:
            try:
                client.load_extension(extension)
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(extension, exc))
        client.run(bot_token)
    except Exception as e:
        # TODO : log error for looking at later
        print('Startup error encountered.')
        print('Exception: {0}: {1}'.format(type(e).__name__, e))
        client.logout()
        sys.exit(0)

