# main.py
# @author Ryan Malacina
# @SnoringNinja - https://snoring.ninja
# Built on discord.py
# Above files not included
# 

# TODO : clean up everything, and by that I mean organize plugins into
#        their own folder and import based on that...possibly just write something to import them all
#        at once based on a config file
# 

import sys

import discord
import asyncio
import spotilib

# Import the plugins folder
# TODO : config to enable / disable plugin files to be imported
import plugins

# Import the commands folder
# TODO : config to enable / disable command files to be imported
import commands

from resources import database

from discord.ext import commands


startup_extensions = ["credit_bet"]

description = '''Betting system for monthly prizes.'''
client = commands.Bot(command_prefix='&', description=description)

# TODO : can we move these out of here? I like the idea of the main file literally just initiating the bot and nothing else
@client.event
async def on_message(message):
    server = message.server
    if (message.content.startswith('!owner')):
        await client.send_message(message.channel, "shaLLow / TD");
    else:
        await client.process_commands(message)

@client.event
async def on_ready():
    # hard set original song
    plugins.MusicHandler().hard_update_current_song()

    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print(plugins.MusicHandler().get_current_song())
    print('------')

    if (plugins.MusicHandler().get_current_song() == 'Spotify'):
        await client.change_presence(game=discord.Game(name='Idle'))
    else:
        await client.change_presence(game=discord.Game(name=plugins.MusicHandler().get_current_song()))

    # This starts the update_song as a background task that will continue to run until we kill it
    client.loop.create_task(plugins.MusicHandler().update_song(client))



if __name__ == "__main__":
    # attempt to connect to the database first before trying anything else
    # try catch for obvious reasons
    print('Checking database before continuing...')
    database.DatabaseHandler().get_conn_details()
    try:
        database.DatabaseHandler().attemptConnection()
        for extension in startup_extensions:
            try:
                client.load_extension(extension)
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(extension, exc))
        client.run('Mjc3ODc0NTUzOTU3NTE1MjY2.C3kGWw.815k4zhNa2HO-CasYs3yCf1XvBI')
        
    except:
        # TODO : log error for looking at later
        print('Database connection failed; killing bot.')
        client.logout()
        sys.exit(0)
