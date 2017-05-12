# Lottery system
# Resets monthly -> for our server, we use this as a way to give out monthly prizes (need to automate this with cron)
# Only runs off executing stored procedures...except, only in a few places...need to extend this to actually be SPs only.

# @TODO : finish
# @TODO : create a function in database that does our generic select one query? Same with credits...
# @TODO : we need to log errors to a file to look at later
# @TODO : error logging decorator

import discord
import logging
from discord.ext import commands
import random
from datetime import datetime
import string
import time
import traceback

from resources.database import DatabaseHandler
from resources.config import ConfigLoader
from resources.error import error_logging

class CreditBet():
	def __init__(self, bot):
		self.bot = bot

		self.channel_id = ConfigLoader().load_config_setting('botsettings', 'channel_id')
		self.server_id = ConfigLoader().load_config_setting('botsettings', 'server_id')

	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(rate=1, per=3, type=commands.BucketType.user)
	async def bet(self, ctx, amount: int, member: discord.Member = None):
		""" Bet if the member exists, otherwise insert them and tell them to reroll. """
		try:
			member = ctx.message.author
			memberID = ctx.message.author.id
			display_name = ctx.message.author.display_name
			if isinstance(amount, int):
				# Have to cast ctx.message.channel.id and ctx.message.server.id to ints
				if (member is not None and amount >= 10 and int(ctx.message.channel.id) == self.channel_id and int(ctx.message.server.id) == self.server_id):
					#print("credit_bet: User: {} / Amount: {} / display_name: {}".format(member, amount, display_name))
					row = DatabaseHandler().fetchresult("""SELECT 1 FROM `users` WHERE `userID` = %s""", (memberID))
					#print("Row: {}".format(row))
					if row is None:
						await self.bot.say("{0.mention}: please do &register to join the lotto.".format(member))
						return
					else:
						#print("Member found, checking remaining credits and generating 'random' numbers for roll.")
						# @TODO : use the system to generate slightly better random numbers...entropy?
						remCredits = DatabaseHandler().fetchresult("""SELECT `credits` FROM `users` WHERE `userID` = %s""", (memberID))
						#print(remCredits)
						if (remCredits[0] < amount):
							await self.bot.say("Insufficient credits ({0})".format(remCredits[0]))
							return
						else:
							botNumber = random.randint(1, 100)
							userNumber = random.randint(1, 100)
							if (botNumber > userNumber):
								args = (str(member), amount, memberID, display_name)
								DatabaseHandler().executeStoredProcedureCommit("RemoveUserCredits", args)
								newBalance = remCredits[0] - amount
								await self.bot.say("Sorry, {0.mention}, you lost with a roll of {1} against {2}! Your balance is now {3}!".format(member, userNumber, botNumber, newBalance))
								#print("User lost. Bot number: {0}, User number: {1}".format(botNumber, userNumber))
							elif (userNumber > botNumber):
								args = (str(member), amount, memberID, display_name)
								DatabaseHandler().executeStoredProcedureCommit("IncreaseUserCredits", args)
								newBalance = remCredits[0] + amount
								await self.bot.say("Congratulations, {0.mention}, you won with a roll of {1} against {2}! Your balance is now {3}!".format(member, userNumber, botNumber, newBalance))
								#print("User won. Bot number: {0}, User number: {1}".format(botNumber, userNumber))
							else:
								await self.bot.say("It was a tie, {0.mention}, with a roll of {1}! Your balance remains {2}!".format(member, userNumber, remCredits[0]))
								#print("Appears a tie...bot number: {0}; user number: {1}".format(botNumber, userNumber))
				else:
					print("Exception in conditional IF statement.")
			else:
				print("Error in bet: Not an int value, but the bot should have caught that by default.")
		except Exception as e:
			error_logging().log_error(traceback.format_exc(), 'credit_bet: bet', str(member))
			print("ERROR! Function: bet. Exception: {0}".format(e))
			await self.bot.say("I failed, sorry...please let TD know (reference: betting error).")

	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(rate=1, per=60, type=commands.BucketType.user)
	async def balance(self, ctx, member: discord.Member = None):
		""" Get balance for user."""
		try:
			# Have to cast ctx.message.channel and ctx.message.server to strings
			if (member is None and int(ctx.message.channel.id) == self.channel_id and int(ctx.message.server.id) == self.server_id):
				member = ctx.message.author
				memberID = ctx.message.author.id
				row = DatabaseHandler().fetchresult("""SELECT 1 FROM `users` WHERE `userID` = %s""", (memberID))
				#print("Row: {}".format(row))
				if row is None:
					await self.bot.say("{0.mention}: please do &register to join the lotto.".format(member))
					return
				else:
					remCredits = DatabaseHandler().fetchresult("""SELECT `credits` FROM `users` WHERE `userID` = %s""", (str(memberID)))
					await self.bot.say("{0.mention}: your balance is {1}.".format(member, remCredits[0]))
		except Exception as e:
			print("ERROR! Function: balance. Exception: {0}".format(e))
			await self.bot.say("I failed, sorry...please let TD know (reference: balance error).")

	@commands.command(pass_context=True, no_pm=True)
	async def register(self, ctx, member: discord.Member = None):
		""" Register member with the bot. """
		try: 
			# Have to cast ctx.message.channel and ctx.message.server to strings
			if (member is None and int(ctx.message.channel.id) == self.channel_id and int(ctx.message.server.id) == self.server_id):
				member = ctx.message.author
				memberID = ctx.message.author.id
				display_name = ctx.message.author.name
				row = DatabaseHandler().fetchresult("""SELECT 1 FROM `users` WHERE `userID` = %s""", (memberID))
				#print("Row: {}".format(row))
				if row is None:
					try:
						#print(member)
						args = (str(member), 500, str(datetime.now()), memberID, display_name)
						#print(args)
						DatabaseHandler().executeStoredProcedureCommit("addMember", args)
						await self.bot.say("{0.mention}, you are now registered! &bet to play! Goodluck!".format(member))
					except Exception as e:
						print("ERROR! Function: register (inner try). Exception: {0}".format(e))
				else:
					await self.bot.say("{0.mention}: you're already registered. Please do &bet to play!".format(member))
		except Exception as e:
			print("ERROR! Function: register. Exception: {0}".format(e))
			await self.bot.say("I failed, sorry...please let TD know (reference: register error).")

	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(rate=1, per=30, type=commands.BucketType.server)
	async def scores(self, ctx, member : discord.Member = None):
		try:
			if (member is None and int(ctx.message.channel.id) == self.channel_id and int(ctx.message.server.id) == self.server_id):
				member = ctx.message.author
				memberID = ctx.message.author.id
				display_name = ctx.message.author.name
				output_string = ''
				
				row = DatabaseHandler().executeStoredProcedureDict("GetTop5",())
				try:
					names = {d['displayName'] for d in row}
					max_name_len = max(map(len, names))
					max_name_len = 22 if max_name_len > 22 else max_name_len
					spacer = max_name_len + 4
					output_string = '```{0: <{1}}  Credits\n'.format('User', spacer)
					output_string = output_string + '{0: <{1}}  -------\n'.format('----', spacer)
					for x in range(len(row)):
						# Add the name and credit amounts of the top 5 users. Truncate usernames at 22 spaces and add '..'
						output_string = output_string + "{0: <{1}}  {2}\n".format(row[x][0][:22] + '..' if len(row[x]['displayName']) > 22 else row[x]['displayName'], spacer, row[x]['credits'])
					output_string = output_string + "\n```"
					await self.bot.say(output_string)
				except Exception as e:
					print(e)
					await self.bot.say("Error: appears no participants found. If this is a mistake, please let TD know.")
		except Exception as e:
			print("ERROR! Function: scores. Exception: {0}".format(e))
			await self.bot.say("I failed, sorry...please let TD know (reference: scores error).")

	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def helpme(self, ctx, member : discord.Member = None):
		""" 100 free credits every 24 hours, if below 500 credits. """
		memberID = ctx.message.author.id
		member = ctx.message.author
		try:
			information = DatabaseHandler().selectAllOptionsParams("""SELECT `credits`, `lastClaimTime` FROM `users` WHERE `userID` = %s""", (str(memberID)))
			currentDate = datetime.now()
			#print(lastUsedTime)
			#print(currentDate)
			member_credits = information[0][0]
			lastUsedTime = information[0][1]
			if member_credits >= 500:
				await self.bot.say("{0.mention}, you are above the maximum threshold to use this command (balance of {1}).".format(member, member_credits))
				return
			else:
				if lastUsedTime is not None:
					total_seconds = (currentDate - lastUsedTime).total_seconds()
					#print(total_seconds)
				if int(total_seconds) >= 86400:
					total_seconds = int(86400 - total_seconds)
					total_hours = int(total_seconds / 3600)
					used_secs = int(total_hours * 3600)
					seconds_left = int(total_seconds - used_secs)
					final_minutes = int(seconds_left / 60)
					formatted_string = "{0}h:{1}m".format(total_hours * -1, final_minutes * -1)
					args = (memberID, str(currentDate))
					DatabaseHandler().executeStoredProcedureCommit("helpMe", args)
					await self.bot.say("{0.mention}, you have been given an additional 100 credits! Your 24 cooldown ended {1} ago!".format(member, formatted_string))
					#print("Helped.")
				else:
					total_seconds = int(86400 - total_seconds)
					total_hours = int(total_seconds / 3600)
					used_secs = int(total_hours * 3600)
					seconds_left = int(total_seconds - used_secs)
					final_minutes = int(seconds_left / 60)
					#print(total_seconds)
					#print(total_hours)
					#print(used_secs)
					#print(seconds_left)
					#print(final_minutes)
					formatted_string = "{0}h:{1}m".format(total_hours, final_minutes)
					await self.bot.say("{0.mention}, you can only use this command every 24 hours ({1}), and if below 500 credits :cry:".format(member, formatted_string))
		except Exception as e:
			print("Exception: {0}".format(e))

def setup(bot):
	"""This makes it so we can actually use it."""
	bot.add_cog(CreditBet(bot))
