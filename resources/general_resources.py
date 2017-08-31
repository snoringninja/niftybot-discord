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
	def __init__(self, bot = None):
		self.prefix = ConfigLoader().load_config_setting('BotSettings', 'command_prefix')

	def checkAccepted(self, user_id, channel_id = None):
		try:
			row = DatabaseHandler().fetch_results("SELECT 1 FROM accepted_users WHERE discord_id = {0}".format(str(user_id)))

			if row is not None:
				return True
			else:
				return False
		except Exception as e:
			error_logging().log_error(traceback.format_exc(), 'BotCommands: checkAccepted')
			return False

	def get_tos_channel_id(self, server_id):
		# Load some config settings
		try:
			try:
				channel_id = ConfigLoader().load_server_config_setting_int(server_id, 'ServerSettings', 'not_accepted_channel_id')
				return True
			except Exception as e:
				error_logging().log_error(traceback.format_exc(), 'BotCommands: get_tos_channel_id')
				return False
		except Exception as e:
			error_logging().log_error(traceback.format_exc(), 'BotCommands: get_tos_channel_id')
			return False