# Lottery system
# Resets monthly -> for our server, we use this as a way to give out monthly prizes
# Only runs off executing stored procedures

# @TODO : finish
# @TODO : how do we want to handle spam? globally limit to only one bet per xxx seconds, or let users run wild...

import discord
from discord.ext import commands
import random

from resources.database import DatabaseHandler

class CreditBet():
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	async def bet(self, ctx, amount: int, member: discord.Member = None):
	""" Bet if the member exists, otherwise insert them and tell them to reroll. """
		try: 
			if isinstance(amount, int):
				if member is None:
					member = ctx.message.author
					print("credit_bet: User: {}".format(member))
					#command_dict = DatabaseHandler().executeStoredProcedure("BuildCommandDictionary", (channel, ))
					row = DatabaseHandler().fetchresult("""SELECT 1 FROM `users` WHERE `username` = %s""", (str(member)))
					print("Row: {}".format(row))
					if row is None:
						print("credit_bet: Member not found, inserting them into the database.")
						try:
							print(member)
							args = (str(member), 500)
							print(args)
							DatabaseHandler().executeStoredProcedureCommit("addMember", args)
							await self.bot.say("Congratulations, {0.mention}, you have been entered into the database! Please redo your bet.".format(member))
						except Exception as e:
							print(e)
					else:
						print("Member found, generating 'random' numbers for roll.")
						# @TODO : use the system to generate slightly better random numbers...entropy?
						botNumber = random.randint(0, 100)
						userNumber = random.randint(0, 100)
						if (butNumber > userNumber):
							# @TODO : subtract bet amount here, or when the bet is made...
							print("User lost. Bot number: {0}, User number: {1}".format(botNumber, userNumber))
						elif (userNumber > botNumber):
							# @TODO : double the bet amount and update the user's credit total
							print("User won. Bot number: {0}, User number: {1}".format(botNumber, userNumber))
						else:
							# @TODO : just return the bet amount to the user...if we only subtract on loss, then do nothing
							print("Appears a tie...bot number: {0}; user number: {1}".format(botNumber, userNumber))
				else:
					print("Error in credit_bet: member was not none.")
			else:
				print("Error in credit_bet: Not an int value, but the bot should have caught that by default.")
		except Exception as e:
			print("Error occured in credit_bet: {}".format(e))
			await self.bot.say("Something went wrong and has been reported to the bot owner.")

def setup(bot):
	"""This makes it so we can actually use it."""
	bot.add_cog(CreditBet(bot))
