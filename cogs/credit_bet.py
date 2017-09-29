# Lottery system type cog

# @TODO : refactor for consistency
# @TODO : document this class completely

import discord
import logging
from discord.ext import commands
import random
from datetime import datetime
import time
import traceback

from resources.database import DatabaseHandler
from resources.config import ConfigLoader
from resources.error import error_logging

from config_updater import ConfigUpdater
from resources.general_resources import BotResources

class CreditBet():
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(rate=1, per=3, type=commands.BucketType.user)
	async def bet(self, ctx, amount: int, member: discord.Member = None):
		""" Let's bet. """
		try:
			member = ctx.message.author
			memberID = ctx.message.author.id
			display_name = ctx.message.author.display_name
			server_id = ctx.message.server.id

			# Load some config settings
			try:
				channel_id = ConfigLoader().load_server_config_setting_int(server_id, 'BettingGame', 'bet_channel_id')
			except Exception as e:
				await ConfigUpdater(self.bot).updateConfigFile(server_id, 'BettingGame', 'enabled', 'False', True)
				return await self.bot.say("The value for channel_id must be a int. Disabling plugin until server owner can correct.")

			# if this fails it's not a boolean so we'll fix that but disable the plugin
			try:
				plugin_enabled = ConfigLoader().load_server_config_setting_boolean(server_id, 'BettingGame', 'enabled')
			except Exception as e:
				await ConfigUpdater(self.bot).updateConfigFile(server_id, 'BettingGame', 'enabled', 'False', True)
				return await self.bot.say("The value for enabled must be a boolean. Disabling plugin until server owner can correct.")

			try:
				minimum_bet = ConfigLoader().load_server_config_setting_int(server_id, 'BettingGame', 'minimum_bet')
			except Exception as e:
				await ConfigUpdater(self.bot).updateConfigFile(server_id, 'BettingGame', 'enabled', 'False', True)
				return await self.bot.say("The value for minimum_bet must be an integer value. Disabling plugin until server owner can correct.")

			if isinstance(amount, int) and plugin_enabled == True and int(ctx.message.channel.id) == channel_id:
				# Have to cast ctx.message.channel.id and ctx.message.server.id to ints
				if (member is not None and amount >= minimum_bet):
					row = DatabaseHandler().fetch_results("SELECT 1 FROM credit_bet WHERE userID = {0} and serverID = {1}".format(str(memberID), str(server_id)))
					if row is None:
						await self.bot.say("{0.mention}: please do &register to join the lotto.".format(member))
						return
					else:
						remCredits = DatabaseHandler().fetch_results("SELECT credits FROM credit_bet WHERE userID = {0} AND serverID = {1}".format(str(memberID), str(server_id)))
						if (remCredits[0] < amount):
							await self.bot.say("Insufficient credits ({0})".format(remCredits[0]))
							return
						else:
							botNumber = random.randint(1, 100)
							userNumber = random.randint(1, 100)
							if (botNumber > userNumber):
								newBalance = remCredits[0] - amount
								DatabaseHandler().update_database("UPDATE credit_bet SET credits = {0} WHERE userID = {1} AND serverID = {2}".format(newBalance, str(memberID), str(server_id)))
								await self.bot.say("Sorry, {0.mention}, you lost with a roll of {1} against {2}! Your balance is now {3}!".format(member, userNumber, botNumber, newBalance))
							elif (userNumber > botNumber):
								newBalance = remCredits[0] + amount
								DatabaseHandler().update_database("UPDATE credit_bet SET credits = {0} WHERE userID = {1} AND serverID = {2}".format(newBalance, str(memberID), str(server_id)))
								await self.bot.say("Congratulations, {0.mention}, you won with a roll of {1} against {2}! Your balance is now {3}!".format(member, userNumber, botNumber, newBalance))
							else:
								await self.bot.say("It was a tie, {0.mention}, with a roll of {1}! Your balance remains {2}!".format(member, userNumber, remCredits[0]))
				else:
					await self.bot.say("The minimum bet is {0}".format(minimum_bet))
			else:
				print("Error in the initial conditional IF statement (credit_bet).")
		except Exception as e:
			await error_logging().log_error(traceback.format_exc(), 'credit_bet: bet', str(member), self.bot)
			await ConfigUpdater(self.bot).updateConfigFile(server_id, 'BettingGame', 'enabled', 'False', True)
			return

	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(rate=1, per=60, type=commands.BucketType.user)
	async def balance(self, ctx, member: discord.Member = None):
		""" Get user balance. """
		member = ctx.message.author
		memberID = ctx.message.author.id
		server_id = ctx.message.server.id

		# Load some config settings
		try:
			channel_id = ConfigLoader().load_server_config_setting_int(server_id, 'BettingGame', 'bet_channel_id')
		except Exception as e:
			await ConfigUpdater(self.bot).updateConfigFile(server_id, 'BettingGame', 'enabled', 'False', True)
			return await self.bot.say("The value for channel_id must be a int. Disabling plugin until server owner can correct.")

		# if this fails it's not a boolean so we'll fix that but disable the plugin
		try:
			plugin_enabled = ConfigLoader().load_server_config_setting_boolean(server_id, 'BettingGame', 'enabled')
		except Exception as e:
			await ConfigUpdater(self.bot).updateConfigFile(server_id, 'BettingGame', 'enabled', 'False', True)
			return await self.bot.say("The value for enabled must be a boolean. Disabling plugin until server owner can correct.")

		try:
			# Have to cast ctx.message.channel and ctx.message.server to strings
			if (member is not None and int(ctx.message.channel.id) == channel_id and plugin_enabled == True):
				row = DatabaseHandler().fetch_results("SELECT 1 FROM credit_bet WHERE userID = {0} and serverID = {1}".format(str(memberID), str(server_id)))
				#print("Row: {}".format(row))
				if row is None:
					await self.bot.say("{0.mention}: please do &register to join the lotto.".format(member))
					return
				else:
					remCredits = DatabaseHandler().fetch_results("SELECT credits FROM credit_bet WHERE userID = {0} AND serverID = {1}".format(str(memberID), str(server_id)))
					await self.bot.say("{0.mention}: your balance is {1}.".format(member, remCredits[0]))
		except Exception as e:
			await error_logging().log_error(traceback.format_exc(), 'credit_bet: register', str(member))
			await ConfigUpdater(self.bot).updateConfigFile(server_id, 'BettingGame', 'enabled', 'False', True)
			await self.bot.say("I failed, sorry...please let TD know (reference: balance error).")

	@commands.command(pass_context=True, no_pm=True)
	async def register(self, ctx, member: discord.Member = None):
		""" Register for betting. """

		member = ctx.message.author
		memberID = ctx.message.author.id
		display_name = ctx.message.author.name
		server_id = ctx.message.server.id

		# Load some config settings
		try:
			channel_id = ConfigLoader().load_server_config_setting_int(server_id, 'BettingGame', 'bet_channel_id')
		except Exception as e:
			await ConfigUpdater(self.bot).updateConfigFile(server_id, 'BettingGame', 'enabled', 'False', True)
			return await self.bot.say("The value for channel_id must be a int. Disabling plugin until server owner can correct.")

		# if this fails it's not a boolean so we'll fix that but disable the plugin
		try:
			plugin_enabled = ConfigLoader().load_server_config_setting_boolean(server_id, 'BettingGame', 'enabled')
		except Exception as e:
			await ConfigUpdater(self.bot).updateConfigFile(server_id, 'BettingGame', 'enabled', 'False', True)
			return await self.bot.say("The value for enabled must be a boolean. Disabling plugin until server owner can correct.")

		try: 
			# Have to cast ctx.message.channel and ctx.message.server to strings
			if (member is not None and int(ctx.message.channel.id) == channel_id and plugin_enabled == True):
				row = DatabaseHandler().fetch_results("SELECT 1 FROM credit_bet WHERE userID = {0} and serverID = {1}".format(str(memberID), str(server_id)))
				if row is None:
					try:
						#print(member)
						args = (str(server_id), str(member), memberID, display_name, 500, str(datetime.now()))
						query = """INSERT INTO credit_bet (serverID, username, userID, displayName, credits, dateJoined, timesBet, lastClaimTime) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
						DatabaseHandler().insert_into_database(query, (str(server_id), str(member), memberID, display_name, 500, str(datetime.now()), 0, str(datetime.now())))
						await self.bot.say("{0.mention}, you are now registered! &bet to play! Goodluck!".format(member))
					except Exception as e:
						await error_logging().log_error(traceback.format_exc(), 'credit_bet: register (inner)', str(member))
				else:
					await self.bot.say("{0.mention}: you're already registered. Please do &bet to play!".format(member))
			else:
				print(member)
				print(ctx.message.channel.id)
				print(channel_id)
				print(plugin_enabled)
		except Exception as e:
			await error_logging().log_error(traceback.format_exc(), 'credit_bet: register (outer)', str(member))
			await self.bot.say("I failed, sorry...please let TD know (reference: register error).")

	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(rate=1, per=30, type=commands.BucketType.server)
	async def scores(self, ctx, member : discord.Member = None):
		""" Display the top 5 with > 0 points. """
		member = ctx.message.author
		memberID = ctx.message.author.id
		display_name = ctx.message.author.name
		server_id = ctx.message.server.id

		# Load some config settings
		try:
			channel_id = ConfigLoader().load_server_config_setting_int(server_id, 'BettingGame', 'bet_channel_id')
		except Exception as e:
			await ConfigUpdater(self.bot).updateConfigFile(server_id, 'BettingGame', 'enabled', 'False', True)
			return await self.bot.say("The value for channel_id must be a int. Disabling plugin until server owner can correct.")

		# if this fails it's not a boolean so we'll fix that but disable the plugin
		try:
			plugin_enabled = ConfigLoader().load_server_config_setting_boolean(server_id, 'BettingGame', 'enabled')
		except Exception as e:
			await ConfigUpdater(self.bot).updateConfigFile(server_id, 'BettingGame', 'enabled', 'False', True)
			return await self.bot.say("The value for enabled must be a boolean. Disabling plugin until server owner can correct.")

		try:
			if (member is not None and int(ctx.message.channel.id) == channel_id and plugin_enabled == True):
				output_string = ''

				try:
					row = DatabaseHandler().fetch_all_results("SELECT displayName, credits, timesBet FROM credit_bet WHERE serverID = {0} ORDER BY credits DESC LIMIT 5".format(str(server_id)))
					names = {d[0] for d in row}
					max_name_len = max(map(len, names))
					max_name_len = 22 if max_name_len > 22 else max_name_len
					spacer = max_name_len + 4
					output_string = '```{0: <{1}}  Credits\n'.format('User', spacer)
					output_string = output_string + '{0: <{1}}  -------\n'.format('----', spacer)
					for x in range(len(row)):
						# Add the name and credit amounts of the top 5 users. Truncate usernames at 22 spaces and add '..'
						output_string = output_string + "{0: <{1}}  {2}\n".format(row[x][0][:22] + '..' if len(row[x][0]) > 22 else row[x][0], spacer, row[x][1])
					output_string = output_string + "\n```"
					await self.bot.say(output_string)
				except Exception as e:
					await error_logging().log_error(traceback.format_exc(), 'credit_bet: scores (inner)', str(member))
					return
		except Exception as e:
			await error_logging().log_error(traceback.format_exc(), 'credit_bet: scores (outer)', str(member))
			return

	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def helpme(self, ctx, member : discord.Member = None):
		""" Free credits for those that qualify. """
		# @TODO : let server owners set time between uses, max amount before preventing, and credits each time
		memberID = ctx.message.author.id
		member = ctx.message.author
		server_id = ctx.message.server.id

		# Load some config settings
		try:
			channel_id = ConfigLoader().load_server_config_setting_int(server_id, 'BettingGame', 'bet_channel_id')
		except Exception as e:
			await ConfigUpdater(self.bot).updateConfigFile(server_id, 'BettingGame', 'enabled', 'False', True)
			return await self.bot.say("The value for channel_id must be a int. Disabling plugin until server owner can correct.")

		# if this fails it's not a boolean so we'll fix that but disable the plugin
		try:
			plugin_enabled = ConfigLoader().load_server_config_setting_boolean(server_id, 'BettingGame', 'enabled')
		except Exception as e:
			await ConfigUpdater(self.bot).updateConfigFile(server_id, 'BettingGame', 'enabled', 'False', True)
			return await self.bot.say("The value for enabled must be a boolean. Disabling plugin until server owner can correct.")

		if plugin_enabled == True and int(ctx.message.channel.id) == channel_id:
			try:
				information = DatabaseHandler().fetch_all_results('SELECT credits, lastClaimTime AS "[timestamp]" FROM credit_bet WHERE userID = {0} AND serverID = {1}'.format(str(memberID), str(server_id)))
				currentDate = datetime.now()
				member_credits = information[0][0]
				lastUsedTime = information[0][1]
				if member_credits >= 500:
					await self.bot.say("{0.mention}, you are above the maximum threshold to use this command (balance of {1}).".format(member, member_credits))
					return
				else:
					if lastUsedTime is not None:
						total_seconds = (currentDate - lastUsedTime).total_seconds()
					if int(total_seconds) >= 86400:
						total_seconds = int(86400 - total_seconds)
						total_hours = int(total_seconds / 3600)
						used_secs = int(total_hours * 3600)
						seconds_left = int(total_seconds - used_secs)
						final_minutes = int(seconds_left / 60)
						formatted_string = "{0}h:{1}m".format(total_hours * -1, final_minutes * -1)
						new_credits = member_credits + 100
						print(currentDate)
						args = (new_credits, str(currentDate), str(memberID), str(server_id), )
						DatabaseHandler().update_database_with_args("UPDATE credit_bet SET credits = ?, lastClaimTime = ? WHERE userID = ? AND serverID = ?", args)
						await self.bot.say("{0.mention}, you have been given an additional 100 credits! Your 24 cooldown ended {1} ago!".format(member, formatted_string))
						return
					else:
						# should we output seconds too?
						total_seconds = int(86400 - total_seconds)
						total_hours = int(total_seconds / 3600)
						used_secs = int(total_hours * 3600)
						seconds_left = int(total_seconds - used_secs)
						final_minutes = int(seconds_left / 60)
						final_seconds = int(seconds_left - (final_minutes * 60))
						formatted_string = "{0}h:{1}m:{2}s".format(total_hours, final_minutes, final_seconds)
						await self.bot.say("{0.mention}, you can only use this command every 24 hours ({1}), and if below 500 credits :cry:".format(member, formatted_string))
						return
			except Exception as e:
				await error_logging().log_error(traceback.format_exc(), 'credit_bet: helpme', str(member))
				return

def setup(bot):
	"""This makes it so we can actually use it."""
	bot.add_cog(CreditBet(bot))
