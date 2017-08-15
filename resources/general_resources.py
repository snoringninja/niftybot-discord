import discord
import logging
from discord.ext import commands
import os
import configparser
import traceback

from resources.database import DatabaseHandler
from resources.config import ConfigLoader
from resources.error import error_logging

class BotResources:
	def __init__(self, bot):
		self.bot = bot
		self.prefix = ConfigLoader().load_config_setting('BotSettings', 'command_prefix')

	def checkAccepted(self, user_id, channel_id = None, show_not_accepted_warning = True):
		try:
			row = DatabaseHandler().fetch_results("SELECT 1 FROM accepted_users WHERE discord_id = {0}".format(str(user_id)))

			if row is not None:
				return True
			else:
				if show_not_accepted_warning == True:
					if channel_id is None:
						self.bot.say(
											"""I'm sorry, you must accept the bot terms of service to use commands.\n\nI may log the following:
											```Your public discord userID\n\nThe ID of the server you used in the command\n\nYour current display name\n\n
											Information provided to me for different functions, including but not limited to: GW2 Api Commands, Credit Betting\n\n```
											Please type {0}accept to accept these terms, which will expand to allow you to use commands in all servers.\n\n
											If this makes you uncomfortable, please check with server owners running me to find out what information they might be logging.""".format(self.prefix)
										  )
					else:
						self.bot.send_message(discord.Object(id=channel_id), """I'm sorry, you must accept the bot terms of service to use commands.\n\nI may log the following:
											```Your public discord userID\n\nThe ID of the server you used in the command\n\nYour current display name\n\n
											Information provided to me for different functions, including but not limited to: GW2 Api Commands, Credit Betting\n\n```
											Please type {0}accept to accept these terms, which will expand to allow you to use commands in all servers.\n\n
											If this makes you uncomfortable, please check with server owners running me to find out what information they might be logging.""".format(self.prefix)
										  )
				return False
		except Exception as e:
			error_logging().log_error(traceback.format_exc(), 'BotCommands: checkAccepted')
			return False