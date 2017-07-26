import discord
from discord.ext import commands
import os, sys

from resources.config import ConfigLoader

class logout():
	def __init__(self, bot):
		self.bot = bot
		self.owner_id = ConfigLoader().load_config_setting_int('BotSettings', 'owner_id')

	@commands.command(pass_context=True, no_pm=True)
	async def logout(self, ctx, member: discord.Member = None):
		userID = ctx.message.author.id

		if int(userID) == self.owner_id:

			await self.bot.say("Shutting down, bye!")
			await self.bot.logout()
		else:
			print(userID)
			return

def setup(bot):
	"""This makes it so we can actually use it."""
	bot.add_cog(logout(bot))
