# Lottery system
# Resets monthly -> for our server, we use this as a way to give out monthly prizes

import discord
from discord.ext import commands
import random

class CreditBet():
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def testing(self, amount : int):
		print("Called.")
		number = random.randint(1, amount)
		await self.bot.say(number)

def setup(bot):
    bot.add_cog(CreditBet(bot))