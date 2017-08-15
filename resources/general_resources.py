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
	def __init__(self):
		self.prefix = ConfigLoader().load_config_setting('BotSettings', 'command_prefix')

	def checkAccepted(self, user_id, channel_id = None, show_not_accepted_warning = True):
		try:
			row = DatabaseHandler().fetch_results("SELECT 1 FROM accepted_users WHERE discord_id = {0}".format(str(user_id)))

			if row is not None:
				return True
			else:
				return False
		except Exception as e:
			error_logging().log_error(traceback.format_exc(), 'BotCommands: checkAccepted')
			return False