# Generate the config file for a server

from resources.config import ConfigGenerator
from resources.config import ConfigLoader
from discord.ext import commands
import discord
import os
from resources.error import error_logging
import traceback

class GenerateConfig():
	def __init__(self, bot):
		self.bot = bot
		self.server_settings_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../channel_settings'))

	@commands.command(pass_context=True, no_pm=True, name='genconfig')
	@commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
	async def generateConfig(self, ctx, member: discord.Member = None):
		member = ctx.message.author
		memberID = ctx.message.author.id
		display_name = ctx.message.author.display_name

		try:
			if memberID == ctx.message.server.owner_id or int(memberID) == ConfigLoader().load_config_setting_int('BotSettings', 'owner_id'):
				file_exists = await ConfigGenerator(self.bot).checkIfConfigExists(ctx.message.server.id)
				if not file_exists:
					await ConfigGenerator(self.bot).generateDefaultConfigFile(ctx.message.server.id, memberID)
				else:
					await self.bot.say("Configuration file already exists.")
			else:
				return
		except Exception as e:
			await error_logging().log_error(traceback.format_exc(), 'GenerateConfig: generateConfig')
			print(e)

def setup(bot):
	"""This makes it so we can actually use it."""
	bot.add_cog(GenerateConfig(bot))