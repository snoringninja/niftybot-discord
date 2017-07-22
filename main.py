# -*- coding: utf-8 -*-

# main.py
# @author Ryan Malacina
# @SnoringNinja - https://snoring.ninja
# Built on discord.py
# Above files not included
# 

# TODO : clean up everything
# TODO : use pickle for setting storage per server instead of one single settings file

import discord
import asyncio
import random

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
database_name = ConfigLoader().load_config_setting('database', 'sqlite')

# TODO : Get listed plugins from settings; not listed = don't use
extension_list = ConfigLoader().load_config_setting('botsettings', 'enabled_plugins')

client = commands.Bot(command_prefix=command_prefix, description=description)
channel_id = ConfigLoader().load_config_setting('botsettings', 'channel_id')

@client.event
async def on_message(message):
    #server = message.server
    #emoteArray = []
    #for x in message.server.emojis:
    #    emoteArray.append(x)
    #print(random.choice(emoteArray))
    #print("Random choice: {0}".format(random.choice(emoteArray)))
    await client.process_commands(message)

@client.event
async def on_ready():
    print('------')
    print('Logged in as {0}; Client ID: {1}'.format(str(client.user.name), str(client.user.id)))
    print('Command prefix is: {0}'.format(str(command_prefix)))
    print('Setting game to: {0}'.format(game_name))
    print('Loaded extensions: {0}'.format(extension_list))
    print('Database name: {0}'.format(database_name))
    await client.change_presence(game=discord.Game(name=game_name))
    print('------')

@client.event
async def on_member_join(member):
    server = member.server
    emoteArray = []
    for x in member.server.emojis:
        emoteArray.append(x)
<<<<<<< HEAD
    #print(emoteArray)
=======
    print(emoteArray)

    # This is throwing errors and needs to be resolved
>>>>>>> 55367437e6ee8fc2e42acfbab886a70be7e1c0a0
    if not emoteArray:
        fmt = 'Welcome to {0.name}\'s Discord, {1.mention}! Relax and have some fun!'.format(server, member)
    else:
        fmt = 'Welcome to {0.name}\'s Discord, {1.mention}! Relax and have some fun! {2}'.format(server, member, random.choice(emoteArray))
    await client.send_message(channel_id, fmt)

if __name__ == "__main__":
    # attempt to connect to the database first before trying anything else
    # try catch for obvious reasons
    # TODO : move this to sqlite and quick check the DB exists before continuing instead of doing SELECT 1 to make sure it can be reached
    print('------')
    print('Checking database before continuing...')
    #database.DatabaseHandler().get_conn_details() if show_db_info == True else False
    error_logging().create_directory()
    try:
        #database.DatabaseHandler().attemptConnection()
        database.DatabaseHandler().connected_to_sqlite()
        print('Connection successful.')

        # @TODO : we need to load all plugins at launch, since per-server configs are going to control plugin access
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
        print(e)
        print('Exception: {0}: {1}'.format(type(e).__name__, e))
        client.logout()
        sys.exit(0)
