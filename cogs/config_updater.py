# Imports for ConfigUpdater
import discord
import logging
from discord.ext import commands
import os
import configparser
import asyncio

from resources.general_resources import BotResources
from resources.config import ConfigLoader
from resources.error import error_logging

class ConfigUpdater:
	def __init__(self, bot):
		self.bot = bot
		self.server_settings_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../channel_settings'))

	def load_config(self, default_filename):
		config = configparser.ConfigParser()
		return config.read(default_filename)

	# Handle updating the config file for the server. supress_message is used when we update the config from a function when a command fails
	# It defaults to False for when the config is updating from within the server
	async def updateConfigFile(self, filename, updateSection, updateKey, updateValue, supress_message=False):

		parser = configparser.ConfigParser()
		loaded_file = self.load_config('%s.ini' % (os.path.join(self.server_settings_path, str(filename))),)
		parser.read(loaded_file)

		try:
			if parser.has_section(updateSection):
				if parser.has_option(updateSection, updateKey):
					parser.set(updateSection, updateKey, updateValue)
					with open('%s.ini' % (os.path.join(self.server_settings_path, str(filename))), 'w') as configfile:
						parser.write(configfile)
					if supress_message == False:
						return await self.bot.say("Configuration file updated successfully (or should have been).")
					else:
						return
				else:
					return await self.bot.say("Key '{0}' does not exist.".format(updateKey))
			else:
				return await self.bot.say("Section '{0}' does not exist.".format(updateSection))
		except Exception as e:
			return await error_logging().log_error(traceback.format_exc(), 'ConfigUpdater: updateConfigFile', str(member), self.bot)

	@commands.command(pass_context=True, no_pm=True, name='config')
	@commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
	async def configUpdate(self, ctx, updateSection: str, updateKey: str, updateValue: str, member: discord.Member = None):
		
		member = ctx.message.author
		memberID = ctx.message.author.id
		display_name = ctx.message.author.display_name

		if memberID == ctx.message.server.owner_id or int(memberID) == ConfigLoader().load_config_setting_int('BotSettings', 'owner_id'):
			try:
				filename = ctx.message.server.id
				await self.updateConfigFile(filename, updateSection, updateKey, updateValue)
			except Exception as e:
				await error_logging().log_error(traceback.format_exc(), 'ConfigUpdater: configUpdate', str(member), self.bot)
				return await self.bot.say("Error applying requested config update: {0}".format(e))
		else:
			return await self.bot.say("Only the server owner can configure different plugins.")

	@commands.command(pass_context=True, no_pm=True, name='getconfig')
	@commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
	async def getConfigInformation(self, ctx, member: discord.Member = None):
		member = ctx.message.author
		memberID = ctx.message.author.id
		serverID = ctx.message.server.id

		try:
			if memberID == ctx.message.server.owner_id or int(memberID) == ConfigLoader().load_config_setting_int('BotSettings', 'owner_id'):
				return_string = "```Settings for {0}:\n\n".format(ctx.message.server.name)

				parser = configparser.ConfigParser()
				loaded_file = self.load_config('%s.ini' % (os.path.join(self.server_settings_path, str(serverID))),)
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
			bot_message = await self.bot.say("I am unable to message you. You may have me blocked, or personal messages disabled.")
			await asyncio.sleep(5)
			await self.bot.delete_message(ctx.message)
			return await self.bot.delete_message(bot_message)
		except Exception as e:
			return await error_logging().log_error(traceback.format_exc(), 'ConfigUpdater: getConfigInformation', str(member), self.bot)

def setup(bot):
	"""This makes it so we can actually use it."""
	bot.add_cog(ConfigUpdater(bot))