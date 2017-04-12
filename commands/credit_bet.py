# Lottery system
# Resets monthly -> for our server, we use this as a way to give out monthly prizes
# Only runs off executing stored procedures

# @TODO : finish
# @TODO : how do we want to handle spam? globally limit to only one bet per xxx seconds, or let users run wild...

import discord
from discord.ext import commands
import random
from datetime import datetime

from resources.database import DatabaseHandler

class CreditBet():
	def __init__(self, bot):
		self.bot = bot
		self.channel_id = 276214890832592897
		#277596190701387777
		
		self.server_id = 224989457445552129
		#171311472855613441

	@commands.command(pass_context=True)
	async def bet(self, ctx, amount: int, member: discord.Member = None):
		""" Bet if the member exists, otherwise insert them and tell them to reroll. """
		try: 
			if isinstance(amount, int):
				# Have to cast ctx.message.channel and ctx.message.server to strings
				if (member is None and int(ctx.message.channel.id) == self.channel_id and int(ctx.message.server.id) == self.server_id):
					member = ctx.message.author
					print("credit_bet: User: {} / Amount: {}".format(member, amount))
					#command_dict = DatabaseHandler().executeStoredProcedure("BuildCommandDictionary", (channel, ))
					row = DatabaseHandler().fetchresult("""SELECT 1 FROM `users` WHERE `username` = %s""", (str(member)))
					print("Row: {}".format(row))
					if row is None:
						await self.bot.say("{0.mention}: please do &register to join the lotto.".format(member))
						return
					else:
						print("Member found, checking remaining credits and generating 'random' numbers for roll.")
						# @TODO : use the system to generate slightly better random numbers...entropy?
						remCredits = DatabaseHandler().fetchresult("""SELECT `credits` FROM `users` WHERE `username` = %s""", (str(member)))
						print(remCredits)
						if (remCredits[0] < amount):
							await self.bot.say("Insufficient credits ({0})".format(remCredits[0]))
							return
						else:
							botNumber = random.randint(0, 100)
							userNumber = random.randint(0, 100)
							if (botNumber > userNumber):
								args = (str(member), amount)
								DatabaseHandler().executeStoredProcedureCommit("RemoveUserCredits", args)
								newBalance = remCredits[0] - amount
								await self.bot.say("Sorry, {0.mention}, you lost with a roll of {1} against {2}! Your balance is now {3}!".format(member, userNumber, botNumber, newBalance))
								print("User lost. Bot number: {0}, User number: {1}".format(botNumber, userNumber))
							elif (userNumber > botNumber):
								args = (str(member), amount)
								DatabaseHandler().executeStoredProcedureCommit("IncreaseUserCredits", args)
								newBalance = remCredits[0] + amount
								await self.bot.say("Congratulations, {0.mention}, you won with a roll of {1} against {2}! Your balance is now {3}!".format(member, userNumber, botNumber, newBalance))
								print("User won. Bot number: {0}, User number: {1}".format(botNumber, userNumber))
							else:
								await self.bot.say("It was a tie, {0.mention}, with a roll of {1}! Your balance remains {2}!".format(member, userNumber, remCredits[0]))
								print("Appears a tie...bot number: {0}; user number: {1}".format(botNumber, userNumber))
				else:
					print("Error in credit_bet: member was not none, channel not test, or server not iBeNifty.")
			else:
				print("Error in credit_bet: Not an int value, but the bot should have caught that by default.")
		except Exception as e:
			print("Error occured in credit_bet: {}".format(e))
			await self.bot.say("I failed, sorry...please let TD know.")

	@commands.command(pass_context=True)
	async def balance(self, ctx, member: discord.Member = None):
		""" Get balannce."""
		try: 
			# Have to cast ctx.message.channel and ctx.message.server to strings
			if (member is None and int(ctx.message.channel.id) == self.channel_id and int(ctx.message.server.id) == self.server_id):
				member = ctx.message.author
				row = DatabaseHandler().fetchresult("""SELECT 1 FROM `users` WHERE `username` = %s""", (str(member)))
				print("Row: {}".format(row))
				if row is None:
					await self.bot.say("{0.mention}: please do &register to join the lotto.".format(member))
					return
				else:
					remCredits = DatabaseHandler().fetchresult("""SELECT `credits` FROM `users` WHERE `username` = %s""", (str(member)))
					await self.bot.say("{0.mention}: your balance is {1}.".format(member, remCredits[0]))
			else:
				print("Error in credit_bet (balance): member was not none, channel not test, or server not iBeNifty.")
		except Exception as e:
			print("Error occured in credit_bet (balance): {}".format(e))
			await self.bot.say("I failed, sorry...please let TD know.")

	@commands.command(pass_context=True)
	async def register(self, ctx, member: discord.Member = None):
		""" Insert user. """
		try: 
			# Have to cast ctx.message.channel and ctx.message.server to strings
			if (member is None and int(ctx.message.channel.id) == self.channel_id and int(ctx.message.server.id) == self.server_id):
				member = ctx.message.author
				row = DatabaseHandler().fetchresult("""SELECT 1 FROM `users` WHERE `username` = %s""", (str(member)))
				print("Row: {}".format(row))
				if row is None:
					try:
						print(member)
						args = (str(member), 500, str(datetime.now()))
						print(args)
						DatabaseHandler().executeStoredProcedureCommit("addMember", args)
						await self.bot.say("Congratulations, {0.mention}, you have been entered into the database! &bet AMOUNT to play!".format(member))
					except Exception as e:
						print(e)
				else:
					await self.bot.say("{0.mention}: you're already registered. Please do &bet AMOUNT to play!".format(member))
			else:
				print("Error in credit_bet(register): member was not none, channel not test, or server not iBeNifty.")
		except Exception as e:
			print("Error occured in credit_bet (register): {}".format(e))
			await self.bot.say("I failed, sorry...please let TD know.")

def setup(bot):
	"""This makes it so we can actually use it."""
	bot.add_cog(CreditBet(bot))
