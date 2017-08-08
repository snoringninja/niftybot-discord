import discord
import logging
from discord.ext import commands

import traceback

from resources.error import error_logging
from resources.config import ConfigLoader

class RoleAssignor():
	def __init__(self, bot):
		self.bot = bot

		self.channel_id_list = ConfigLoader().load_config_setting('RoleAssignment', 'role_channel_list')
		self.server_id = ConfigLoader().load_config_setting('BotSettings', 'server_id')
		self.role_list = ConfigLoader().load_config_setting('RoleAssignment', 'role_list')

	@commands.command(pass_context=True, no_pm=False, name='guild')
	@commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
	async def assign_role(self, ctx, guild : str, member: discord.Member = None):

		try:
			member = ctx.message.author
			requested_guild = discord.utils.get(ctx.message.server.roles, name=guild)

			if member is not None:
				channel_list = []
				for role in map(int, self.channel_id_list.split()):
					channel_list.append(role)

				#print(channel_list)

				if requested_guild is not None:
					requested_guild_id = int(requested_guild.id)

					role_list_split = []
					for role in map(int, self.role_list.split()):
						role_list_split.append(role)

					#print(role_list_split)
					#print(requested_guild.name)
					#print(requested_guild.id)

					# yes, we do this check somewhat twice
					#if requested_guild_id in role_list_split:
					#	print("Yes.")

					if int(ctx.message.channel.id) in channel_list:
						if requested_guild_id in role_list_split:
							try:

								# loop through the roles the user has
								for r in ctx.message.author.roles:
									# must cast to int for this to work
									if int(r.id) == requested_guild_id:
										print("{0} was already in the requested guild.".format(member))
										#await self.bot.send_message(ctx.message.channel, "{0.mention}: You're already assigned to a guild. Please contact an alliance moderator or lord to reset the guild if incorrect.".format(ctx.message.author))
										await self.bot.send_message(ctx.message.channel, "{0.mention}: You're already assigned to this guild.".format(member))
										return
									
								await self.bot.add_roles(ctx.message.author, requested_guild)
								await self.bot.send_message(ctx.message.channel, "{0.mention}: You've been successfully added to {1}!".format(member, requested_guild.name))
								return
							except:
								await self.bot.send_message(ctx.message.channel, "Error.")
								error_logging().log_error(traceback.format_exc(), 'role_assignment: assign_role', str(member))
								return
							finally:
								print("Finally block executed.")
						else:
							await self.bot.send_message(ctx.message.channel, "{0.mention}: Requested guild not found.".format(member))
							return
					else:
						print("Channel not in list.")
						return
				else:
					return
			else:
				print("Member was none.")
				return
		except Exception as e:
			error_logging().log_error(traceback.format_exc(), 'assign_role: RoleAssignor', str(member))
			await self.bot.say("Error with the given API key. Please check it again.")
			return

def setup(bot):
	"""This makes it so we can actually use it."""
	bot.add_cog(RoleAssignor(bot))