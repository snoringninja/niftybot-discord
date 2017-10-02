import discord
import logging
from discord.ext import commands

import traceback

from resources.error import ErrorLogging
from resources.config import ConfigLoader

from cogs.config_updater import ConfigUpdater

class RoleAssignor():
	def __init__(self, bot):
		self.bot = bot

	def contains_word(self, s, w):
		return (' ' + w + ' ') in (' ' + s + ' ')

	@commands.command(pass_context=True, no_pm=False, name='guild')
	@commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
	async def assign_role(self, ctx, guild : str, member: discord.Member = None):

		server_id = ctx.message.server.id
		member = ctx.message.author
		memberID = ctx.message.author.id
		display_name = ctx.message.author.display_name

		# if this fails it's not a boolean so we'll fix that but disable the plugin
		try:
			plugin_enabled = ConfigLoader().load_server_config_setting_boolean(server_id, 'RoleAssignment', 'enabled')
		except Exception as e:
			await ConfigUpdater(self.bot).updateConfigFile(server_id, 'RoleAssignment', 'enabled', 'False', True)
			return await self.bot.say("The value for enabled must be a boolean. Disabling plugin until server owner can correct.")

		try:
			member = ctx.message.author

			if member is not None and plugin_enabled == True:
				requested_guild = discord.utils.get(ctx.message.server.roles, name=guild)

				role_list = ConfigLoader().load_server_config_setting(server_id, 'RoleAssignment', 'role_list')
				assignment_channel_list = ConfigLoader().load_server_config_setting(server_id, 'RoleAssignment', 'assignment_channel_id')

				if assignment_channel_list == 'NOT_SET':
					return await self.bot.say("The server owner needs to configure channels for this command.")

				if role_list == 'NOT_SET':
					return await self.bot.say("The server owner needs to configure roles.")

				channel_list = []
				for channel in map(int, assignment_channel_list.split()):
					channel_list.append(channel)

				if requested_guild is not None:
					requested_guild_id = int(requested_guild.id)

					role_list_split = []
					for role in map(int, role_list.split()):
						role_list_split.append(role)

					if int(ctx.message.channel.id) in channel_list:
						if requested_guild_id in role_list_split:
							try:

								# loop through the roles the user has
								for r in ctx.message.author.roles:
									# must cast to int for this to work
									if int(r.id) == requested_guild_id:
										await self.bot.send_message(ctx.message.channel, "{0.mention}: You're already assigned to this group.".format(member))
										return
									
								await self.bot.add_roles(ctx.message.author, requested_guild)
								await self.bot.send_message(ctx.message.channel, "{0.mention}: You've been successfully added to {1}!".format(member, requested_guild.name))
								return
							except:
								await self.bot.send_message(ctx.message.channel, "Error.")
								await ErrorLogging().log_error(traceback.format_exc(), 'role_assignment: assign_role', str(member))
								return
						else:
							await self.bot.send_message(ctx.message.channel, "{0.mention}: Requested group not found.".format(member))
							return
					else:
						return
				else:
					return
			else:
				return
		except Exception as e:
			await ErrorLogging().log_error(traceback.format_exc(), 'role_assignment: RoleAssignor', str(member))
			return

	@commands.command(pass_context=True, no_pm=False, name='role')
	@commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
	async def updateRoleList(self, ctx, add_or_remove: str, role_id: str, member: discord.Member = None):

		try:
			member = ctx.message.author
			server_id = str(ctx.message.server.id)

			if member is not None:
				if add_or_remove != 'add' and add_or_remove != 'remove':
					return await self.bot.say("Please specify if I am adding or removing a role.")

				current_role_list = ConfigLoader().load_server_config_setting(server_id, 'RoleAssignment', 'role_list')

				if add_or_remove == 'add':
					if not self.contains_word(current_role_list, role_id):
						if current_role_list == 'NOT_SET':
							updated_role_list = role_id
						else:
							updated_role_list = current_role_list + " " + role_id
					else:
						return await self.bot.say("Role already added.")

				if add_or_remove == 'remove':
					if self.contains_word(current_role_list, role_id):
						updated_role_list = current_role_list.strip(' ' + role_id + ' ')

				if updated_role_list.isspace() or len(updated_role_list) == 0:
					updated_role_list = 'NOT_SET'

				filename = ctx.message.server.id
				await ConfigUpdater(self.bot).updateConfigFile(filename, 'RoleAssignment', 'role_list', updated_role_list.strip())
		except Exception as e:
			await ErrorLogging().log_error(traceback.format_exc(), 'role_assignment: updateRoleList', str(member))
			return

	@commands.command(pass_context=True, no_pm=False, name='rolechannel')
	@commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
	async def updateChannelList(self, ctx, add_or_remove: str, channel_id: str, member: discord.Member = None):

		try:
			member = ctx.message.author
			server_id = str(ctx.message.server.id)

			if member is not None:
				if add_or_remove != 'add' and add_or_remove != 'remove':
					return await self.bot.say("Please specify if I am adding or removing a channel.")

				current_channel_list = ConfigLoader().load_server_config_setting(server_id, 'RoleAssignment', 'assignment_channel_id')

				if add_or_remove == 'add':
					if not self.contains_word(current_channel_list, channel_id):
						if current_channel_list == 'NOT_SET':
							updated_channel_list = channel_id
						else:
							updated_channel_list = current_channel_list + " " + channel_id
					else:
						return await self.bot.say("Channel already added.")

				if add_or_remove == 'remove':
					if self.contains_word(current_channel_list, channel_id):
						updated_channel_list = current_channel_list.strip(' ' + channel_id + ' ')

				if updated_channel_list.isspace() or len(updated_channel_list) == 0:
					updated_channel_list = 'NOT_SET'

				filename = ctx.message.server.id
				await ConfigUpdater(self.bot).updateConfigFile(filename, 'RoleAssignment', 'assignment_channel_id', updated_channel_list.strip())
		except Exception as e:
			await ErrorLogging().log_error(traceback.format_exc(), 'role_assignment: updateChannelList', str(member))
			return



def setup(bot):
	"""This makes it so we can actually use it."""
	bot.add_cog(RoleAssignor(bot))