# music_handler
# Makes use of spotilib, will need to download it manually and copy to the Lib folder
# 	as there is no pip install for it.

import discord
import asyncio
import spotilib

class MusicHandler():
	""" 
	This only works on a local machine that can run Spotify
	I thought about utilizing Scrobble, but I hate last.fm with a passion

	Anyways, while running, we check the current_song and
	compare against next_song. If different, update based on criteria.

	If the same, do nothing to prevent flooding change_presence and timing the bot out

	@TODO : look into possibly sending song off to something
			and using an API to grab from there so we can run this on a dedicated VPS

	@TODO : quickly switching songs can cause the bot to stop changing songs; possibly
			able to alleviate this by increasing the time to 5 seconds vs. the 3 seconds
			that currently is; needs to be tested
	"""
	def __init__(self):

		# The currently playing song
		self.current_song = ''

		# This is the variable getting updated every call to the update_song (assuming it's different)
		self.next_song = ''

		# Flag for flood prevention
		self.song_needs_update = False

	@classmethod
	def update_current_song(self, next_song):
		self.current_song = next_song

	@classmethod
	def hard_update_current_song(self):
		#print("Called.")
		x = spotilib.song_info()
		if (x != ''):
			self.current_song = x
		else:
			self.current_song = 'Forcing proper update.'

	@classmethod
	def update_next_song(self):
		x = spotilib.song_info()
		if (x != ''):
			self.next_song = x
		else:
			self.next_song = ''

	@classmethod
	def get_current_song(self):
		return self.current_song

	@classmethod
	def get_next_song(self):
		return self.next_song

	@classmethod
	def compare_songs(self):
		self.update_next_song()
		if (self.get_current_song() != self.get_next_song()):
			self.update_current_song(self.get_next_song())
			self.song_needs_update = True
			print("Updating song to {}.".format(self.get_next_song()))
			return True
		else:
			self.song_needs_update = False
			return False

	@classmethod
	async def update_song(self, client):
		"""
			We pass in the client created in the main.py file to allow us to
			update the game being played

			@TODO : catch errors and do something
		"""

		# Just a debugging statement to make sure this was getting called
		print("initial call.")

		# Keep running as long as the client is connected
		while not client.is_closed:

			# Now we do the logic checks
			# NOTE: this is on a 3 second asyncio sleep, I don't really see a need to go lower...
			# 		5 seconds could possibly be better
			if (self.compare_songs()):
				if (self.get_current_song() != 'Spotify' and self.get_current_song() != ''):
					await client.change_presence(game=discord.Game(name=self.get_current_song()))
				elif (self.get_current_song() == 'Spotify' and self.song_needs_update == True):
					#print("Updating song to 'Idle'.")
					self.update_current_song('Spotify')
					await client.change_presence(game=discord.Game(name='Idle'))
				else:
					if (self.song_needs_update == True):
						#print("Unknown error (Spotify not running?) encountered.")
						await client.change_presence(game=discord.Game(name='Spotify not loaded.'))
				await asyncio.sleep(3)
			else:
				# I don't recommend printing the following out, it'll just spam the console.
				# print("Song update was skipped.")
				await asyncio.sleep(3)
