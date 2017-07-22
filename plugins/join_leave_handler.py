from resources.resourcepath import *
from resources.config import ConfigLoader
from resources.error import error_logging
import discord
import string
import time
import traceback
import random

class JoinLeaveHandler():
	def __init__(self, bot):
		self.bot = bot

	async def welcomeUser(self, server_id : str, member : str, server : str):
		try:
			welcome_channel = ConfigLoader().load_server_config_setting(server_id, 'join_part', 'welcome_channel_id')
			display_name = member.display_name

			emoteArray = []
			for x in member.server.emojis:
				emoteArray.append(x)

			await self.bot.send_message(discord.Object(id=welcome_channel), "Welcome to {0.name}\'s Discord, {1.mention}! Relax and have some fun! {2}".format(server, member, random.choice(emoteArray)))
		except Exception as e:
			error_logging().log_error(traceback.format_exc(), 'join_leave_handler: welcomeUser', str(member))
			return

	async def goodbyeUser(self, server_id : str, member : str):
		try:
			part_channel = ConfigLoader().load_server_config_setting(server_id, 'join_part', 'leave_channel_id')
			display_name = member.display_name

			await self.bot.send_message(discord.Object(id=part_channel), "{0} ({1}) has left the server.".format(member, display_name))
		except Exception as e:
			error_logging().log_error(traceback.format_exc(), 'join_leave_handler: goodbyeUser', str(member))
			return
