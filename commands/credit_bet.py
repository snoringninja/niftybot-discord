# Lottery system
# Resets monthly -> for our server, we use this as a way to give out monthly prizes
# Only runs off executing stored procedures

# @TODO : finish
# @TODO : how do we want to handle spam? globally limit to only one bet per xxx seconds, or let users run wild...
# @TODO : use ConfigLoader
# @TODO : create a function in database that does our generic select one query? Same with credits...

import discord
import logging
from discord.ext import commands
import random
from datetime import datetime

from resources.database import DatabaseHandler

class CreditBet():
	def __init__(self, bot):
		# TODO : import from config if we are in debug, and swap channel_id and server_id depending
		self.bot = bot

		self.channel_id = 277596190701387777 #276214890832592897
		#277596190701387777

		self.server_id = 171311472855613441 #224989457445552129
		#171311472855613441

	@commands.command(pass_context=True, no_pm=True)
	async def bet(self, ctx, amount: int, member: discord.Member = None):
		""" Bet if the member exists, otherwise insert them and tell them to reroll. """
		try:
			if isinstance(amount, int):
				# Have to cast ctx.message.channel.id and ctx.message.server.id to ints
				if (member is None and amount >= 10 and int(ctx.message.channel.id) == self.channel_id and int(ctx.message.server.id) == self.server_id):
					member = ctx.message.author
					memberID = ctx.message.author.id
					display_name = ctx.message.author.name
					#print("credit_bet: User: {} / Amount: {}".format(member, amount))
					#command_dict = DatabaseHandler().executeStoredProcedure("BuildCommandDictionary", (channel, ))
					row = DatabaseHandler().fetchresult("""SELECT 1 FROM `users` WHERE `userID` = %s""", (memberID))
					#print("Row: {}".format(row))
					if row is None:
						await self.bot.say("{0.mention}: please do &register to join the lotto.".format(member))
						return
					else:
						print("Member found, checking remaining credits and generating 'random' numbers for roll.")
						# @TODO : use the system to generate slightly better random numbers...entropy?
						remCredits = DatabaseHandler().fetchresult("""SELECT `credits` FROM `users` WHERE `userID` = %s""", (memberID))
						#print(remCredits)
						if (remCredits[0] < amount):
							await self.bot.say("Insufficient credits ({0})".format(remCredits[0]))
							return
						else:
							botNumber = random.randint(0, 100)
							userNumber = random.randint(0, 100)
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
				print("Error in credit_bet: Not an int value, but the bot should have caught that by default.")
		except Exception as e:
			print("ERROR! Function: credit_bet. Exception: {0}".format(e))
			await self.bot.say("I failed, sorry...please let TD know (reference: betting error).")

	@commands.command(pass_context=True, no_pm=True)
	async def balance(self, ctx, member: discord.Member = None):
		""" Get balance for user."""
		try:
			# Have to cast ctx.message.channel and ctx.message.server to strings
			if (member is None and int(ctx.message.channel.id) == self.channel_id and int(ctx.message.server.id) == self.server_id):
				member = ctx.message.author
				memberID = ctx.message.author.id
				row = DatabaseHandler().fetchresult("""SELECT 1 FROM `users` WHERE `userID` = %s""", (memberID))
				print("Row: {}".format(row))
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
						await self.bot.say("{0.mention}, you have now been entered into the database! &bet AMOUNT to play! Goodluck!".format(member))
					except Exception as e:
						print("ERROR! Function: register (inner try). Exception: {0}".format(e))
				else:
					await self.bot.say("{0.mention}: you're already registered. Please do &bet AMOUNT to play!".format(member))
		except Exception as e:
			print("ERROR! Function: register. Exception: {0}".format(e))
			await self.bot.say("I failed, sorry...please let TD know (reference: register error).")

	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(2, 60, commands.BucketType.user)
	async def scores(self, ctx, member : discord.Member = None):
		try:
			if (member is None and int(ctx.message.channel.id) == self.channel_id and int(ctx.message.server.id) == self.server_id):
				member = ctx.message.author
				memberID = ctx.message.author.id
				display_name = ctx.message.author.name
				output_string = ''
				# This is pretty stupid...I should really redo so I only need one database select.
				#row = DatabaseHandler().selectAllOptions("""SELECT `displayName`, `credits`, `timesBet` FROM `users` WHERE `credits` > 0 ORDER BY `credits` DESC LIMIT 5""")
				row = DatabaseHandler().executeStoredProcedure("GetTop5",())
				row2 = DatabaseHandler().selectAllOptionsDict("""SELECT `displayName`, `credits`, `timesBet` FROM `users` ORDER BY `credits` DESC LIMIT 5""")
				names = {d['displayName'] for d in row2}
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
			print("ERROR! Function: scores. Exception: {0}".format(e))
			await self.bot.say("I failed, sorry...please let TD know (reference: scores error).")

	@commands.command(pass_context=True, no_pm=True)
	async def helpme(self, ctx, member : discord.Member = None):
		""" 100 free credits every 24 hours. """
		# @TODO : once a user hits the amount given for a register, don't allow them to use the command (alongside 24 hour cooldown)
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
				await self.bot.say("{0.mention}, you are above the minimum threshhold for using this command (balance of {1}).".format(str(member), member_credits))
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
					await self.bot.say("{0.mention}, you have been given an additional 100 credits! You were eligible {1} ago!".format(member, formatted_string))
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
					await self.bot.say("{0.mention}, you can only use this command every 24 hours ({1}) :middle_finger:".format(member, formatted_string))
		except Exception as e:
			print("Exception: {0}".format(e))

def setup(bot):
	"""This makes it so we can actually use it."""
	bot.add_cog(CreditBet(bot))
