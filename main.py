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

import discord
import asyncio
import spotilib

# Show what song is playing on the local Spotify
# from music_handler import MusicHandler

import plugins

client = discord.Client()

@client.event
async def on_message(message):
    server = message.server
    if (message.content.startswith('!owner')):
        await client.send_message(message.channel, "shaLLow / TD");

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

client.run('Mjc3ODc0NTUzOTU3NTE1MjY2.C3kGWw.815k4zhNa2HO-CasYs3yCf1XvBI')
