# Lottery system
# Resets monthly -> for our server, we use this as a way to give out monthly prizes

import discord
from discord.ext import commands
import random

from resources import database

class CreditBet():
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	async def bet(self, ctx, amount: int, member: discord.Member = None):
		try: 
			if isinstance(amount, int):
				if member is None:
					member = ctx.message.author
					print("User: {}...".format(member))
				else:
					print("Error: member was not none.")
		except Exception as e: 
			await self.bot.say("Integer values only.")

def setup(bot):
    bot.add_cog(CreditBet(bot))