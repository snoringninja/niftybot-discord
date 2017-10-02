# Imports for ConfigUpdater
import discord
import logging
from discord.ext import commands
import os
import configparser
import traceback

from resources.database import DatabaseHandler
from resources.config import ConfigLoader
from resources.error import ErrorLogging
from resources.general_resources import BotResources

class BotCommands:
	def __init__(self, bot):
		self.bot = bot
		self.prefix = ConfigLoader().load_config_setting('BotSettings', 'command_prefix')

	@commands.command(pass_context=True, no_pm=False, name='accept')
	@commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
	async def add_accepted_user(self, ctx, member: discord.Member = None):
		member = ctx.message.author
		memberID = ctx.message.author.id

		try:
			has_accepted = BotResources().checkAccepted(memberID, False)

			if has_accepted == True:
				return await self.bot.say("You've already accepted my terms of service.")
			else:
				try:
					query = """INSERT INTO accepted_users (discord_id) VALUES (?)"""
					DatabaseHandler().insert_into_database(query, (str(memberID), ))
					return await self.bot.say("{0.mention}: thanks for accepting. You may now use commands.".format(member))
				except Exception as e:
					await ErrorLogging().log_error(traceback.format_exc(), 'BotCommands: add_accepted_user')
		except Exception as e:
			await ErrorLogging().log_error(traceback.format_exc(), 'BotCommands: add_accepted_user')

	@commands.command(pass_context=True, no_pm=True, name='nick')
	@commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
	async def change_username(self, ctx, username: str, member: discord.Member = None):
		member = ctx.message.author
		memberID = ctx.message.author.id

		try:
			if memberID == ctx.message.server.owner_id or int(memberID) == ConfigLoader().load_config_setting_int('BotSettings', 'owner_id'):
				await self.bot.change_nickname(ctx.message.server.me, username)
				return await self.bot.say("Changed my username!")
		except Exception as e:
			await ErrorLogging().log_error(traceback.format_exc(), 'BotCommands: change_username')

	@commands.command(pass_context=True, no_pm=True, name="help")
	@commands.cooldown(rate=1, per=30, type=commands.BucketType.server)
	async def get_help(self, ctx, member: discord.Member = None):
		member = ctx.message.author
		memberID = ctx.message.author.id

		return await self.bot.say("{0.mention}: Please see https://xnifty.github.io for now.".format(member))

def setup(bot):
	"""This makes it so we can actually use it."""
	bot.add_cog(BotCommands(bot))