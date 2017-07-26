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
		welcome_enabled = ConfigLoader().load_server_config_setting_boolean(server_id, 'JoinPart', 'member_join_enabled')

		try:
			if welcome_enabled == True:
				welcome_channel = ConfigLoader().load_server_config_setting(server_id, 'JoinPart', 'welcome_channel_id')
				display_name = member.display_name

				emoteArray = []
				for x in member.server.emojis:
					emoteArray.append(x)

				if not emoteArray:
					await self.bot.send_message(discord.Object(id=welcome_channel), "Welcome to {0.name}\'s Discord, {1.mention}! Relax and have some fun!".format(server, member))
				else:
					await self.bot.send_message(discord.Object(id=welcome_channel), "Welcome to {0.name}\'s Discord, {1.mention}! Relax and have some fun! {2}".format(server, member, random.choice(emoteArray)))
			else:
				print("Welcome message disabled.")
				return
		except Exception as e:
			error_logging().log_error(traceback.format_exc(), 'join_leave_handler: welcomeUser', str(member))
			return

	async def goodbyeUser(self, server_id : str, member : str):
		part_enabled = ConfigLoader().load_server_config_setting_boolean(server_id, 'JoinPart', 'member_part_enabled')

		try:
			if part_enabled == True:
				part_channel = ConfigLoader().load_server_config_setting(server_id, 'JoinPart', 'leave_channel_id')
				display_name = member.display_name

				await self.bot.send_message(discord.Object(id=part_channel), "{0} ({1}) has left the server.".format(member, display_name))
			else:
				print("Part message disabled.")
				return
		except Exception as e:
			error_logging().log_error(traceback.format_exc(), 'join_leave_handler: goodbyeUser', str(member))
			return