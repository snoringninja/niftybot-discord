import discord
from discord.ext import commands

class logout():
	def __init__(self, bot):
		self.bot = bot
		self.owner_id = 104771621687980032

	@commands.command(pass_context=True, no_pm=True)
	async def logout(self, ctx, member: discord.Member = None):
		userID = ctx.message.author.id
		print(userID)
		if int(userID) == self.owner_id:
			await self.bot.say("Shutting down, bye!")
			await self.bot.logout()
		else:
			return

def setup(bot):
	"""This makes it so we can actually use it."""
	bot.add_cog(logout(bot))
