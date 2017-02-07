# main.py
# @author Ryan Malacina
# @SnoringNinja - https://snoring.ninja
# Built on discord.py

import discord
import asyncio
import spotilib

from music_handler import MusicHandler

client = discord.Client()

@client.event
async def on_message(message):
    server = message.server
    # if message.content.startswith('!test'):
    #     counter = 0
    #     tmp = await client.send_message(message.channel, 'Calculating messages...')
    #     async for log in client.logs_from(message.channel, limit=100):
    #         if log.author == message.author:
    #             counter += 1

    #     await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    # elif message.content.startswith('!sleep'):
    #     await asyncio.sleep(5)
    #     await client.send_message(message.channel, 'Done sleeping')
    if (message.content.startswith('!kill_bot')):# and 
        if (message.author == 'shaLLow#8086'):
            print("Shut down received.")
            await client.send_message(message.channel, "Shutting down...")
            await client.logout()
    if (message.content.startswith('!owner')):
        await client.send_message(message.channel, "shaLLow / TD");

@client.event
async def on_ready():
    # hard set original song
    MusicHandler().hard_update_current_song()

    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print(MusicHandler().get_current_song())
    print('------')

    if (MusicHandler().get_current_song() == 'Spotify'):
        await client.change_presence(game=discord.Game(name='Awaiting Music'))
    else:
        await client.change_presence(game=discord.Game(name=MusicHandler().get_current_song()))

    # This starts the update_song as a background task that will continue to run until we kill it
    client.loop.create_task(MusicHandler().update_song(client))

client.run('Mjc3ODc0NTUzOTU3NTE1MjY2.C3kGWw.815k4zhNa2HO-CasYs3yCf1XvBI')
