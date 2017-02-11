# Lottery system
# Resets monthly -> for our server, we use this as a way to give out monthly prizes
# Only runs of executing stored procedures

# TODO : finish

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
					print("User: {}".format(member))
					#command_dict = DatabaseHandler().executeStoredProcedure("BuildCommandDictionary", (channel, ))
					row = DatabaseHandler().fetchresult("""SELECT 1 FROM `users` WHERE `username` = %s""", (str(member)))
					print("Row: {}".format(row))
					if row is None:
						print("Member not found; todo: insert user into database and allocate credits")
						try:
							print(member)
							args = (str(member), 500)
							print(args)
							DatabaseHandler().executeStoredProcedureCommit("addMember", args)
							await self.bot.say("Congratulations, {0.mention}, you have been entered into the database! Please redo your bet.".format(member))
						except Exception as e:
							print(e)
					else:
						print("Member found.")
				else:
					print("Error: member was not none.")
			else:
				print("Not an int value, but the bot should have caught that by default.")
		except Exception as e: 
			await self.bot.say("Error occured: {}".format(e))

def setup(bot):
    bot.add_cog(CreditBet(bot))