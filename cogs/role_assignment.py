"""
role_assignment.py
@author xNifty
@site https://snoring.ninja

Handles all role assignment based commands
"""

import traceback
import logging

from resources.error_logger import ErrorLogging
from resources.config import ConfigLoader

from cogs.config_commands import ConfigCommands

import discord
from discord.ext import commands

def contains_word(string, word):
    """Check if a word exists inside the string.

    @TODO: allow user to remove themselves from any of the configured
    groups that they are able to add themselves to

    @TODO: allow owners to add roles/channels simply by passing in the
    name of the role or channel instead of requiring them to use the
    snowflake ID; if there happens to be more than one of either, then
    require the owner to use the specific ID
    """
    return ' ' + word + ' ' in ' ' + string + ' '

class RoleAssignor():
    """RoleAssignor

    Handles commands for adding or removing a role, adding or
    removing a channel, or adding a user to a configured role
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=False, name='guild')
    @commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
    async def assign_role(self, ctx, guild: str, member: discord.Member=None):
        """Assign users to configured roles if requested

        :guild: the requested group name
        :member: empty discord.Member object
        """
        server_id = ctx.message.server.id
        member = ctx.message.author

        plugin_enabled = ConfigLoader().load_server_boolean_setting(
            server_id,
            'RoleAssignment',
            'enabled'
        )

        member = ctx.message.author

        if member is not None and plugin_enabled:
            requested_guild = discord.utils.get(ctx.message.server.roles, name=guild)

            role_list = ConfigLoader().load_server_string_setting(
                server_id,
                'RoleAssignment',
                'role_list'
            )

            assignment_channel_list = ConfigLoader().load_server_string_setting(
                server_id,
                'RoleAssignment',
                'assignment_channel_id'
            )

            if role_list == 'NOT_SET' or assignment_channel_list == 'NOT_SET':
                return await self.bot.say("This plugin is not configured for this server.")

            channel_list = []
            for channel in map(int, assignment_channel_list.split()):
                channel_list.append(channel)

            if requested_guild is not None:
                requested_guild_id = int(requested_guild.id)

                role_list_split = []
                for role in map(int, role_list.split()):
                    role_list_split.append(role)

                if int(ctx.message.channel.id) in channel_list and \
                requested_guild_id in role_list_split:
                    for role in ctx.message.author.roles:
                        if int(role.id) == requested_guild_id:
                            await self.bot.send_message(
                                ctx.message.channel,
                                "{0.mention}: You're already assigned to this " \
                                "group.".format(
                                    member
                                )
                            )
                        else:
                            await self.bot.add_roles(ctx.message.author, requested_guild)
                            await self.bot.send_message(
                                ctx.message.channel,
                                "{0.mention}: You've been successfully " \
                                "added to {1}!".format(member, requested_guild.name))
                        return
                else:
                    return
            else:
                return
        else:
            return

    @commands.command(pass_context=True, no_pm=False, name='role')
    @commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
    async def update_role_list(self, ctx, add_or_remove: str, \
                               role_id: str, member: discord.Member=None
                              ):
        """Update the configured role list to add or remove
        a group.

        :add_or_remove: (str) [add, remove] passed in string to determine
        if a role is being added or removed

        :role_id: the discord snowflake ID for the role, the pinged username
        :member: empty discord.Member object
        """
        member = ctx.message.author
        server_id = str(ctx.message.server.id)

        if member is not None:
            if add_or_remove != 'add' and add_or_remove != 'remove':
                return await self.bot.say("Please specify if I am adding or removing a role.")

            current_role_list = ConfigLoader().load_server_string_setting(
                server_id,
                'RoleAssignment',
                'role_list'
            )

            # Hacky fix for when mentioning the role to strip stuff out
            role_id = role_id.replace('<@&', '')
            role_id = role_id.replace('>', '')
            role_id = role_id.strip()

            if add_or_remove == 'add':
                if not contains_word(current_role_list, role_id):
                    if current_role_list == 'NOT_SET':
                        updated_role_list = role_id
                    else:
                        updated_role_list = current_role_list + " " + role_id
                else:
                    return await self.bot.say("Role already added.")

            if add_or_remove == 'remove':
                if contains_word(current_role_list, role_id):
                    updated_role_list = current_role_list.replace(role_id, '')

                if updated_role_list.isspace() or len(updated_role_list) == 0:
                    updated_role_list = 'NOT_SET'

            filename = ctx.message.server.id
            await ConfigCommands(self.bot).update_config_file(
                filename,
                'RoleAssignment',
                'role_list',
                updated_role_list.strip(),
                ctx.message
            )

@commands.command(pass_context=True, no_pm=False, name='rolechannel')
@commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
async def update_channel_list(self, ctx, add_or_remove: str, \
                              channel_id: str, member: discord.Member=None
                             ):
    """Update the configured channel list to
    add or remove a channel where the guild command can be used

    :add_or_remove: (str) [add, remove] passed in string to determine
    if a channel is being added or removed

    :channel_id: the discord snowflake ID for the channel
    :member: empty discord.Member object
    """
    member = ctx.message.author
    server_id = str(ctx.message.server.id)

    if member is not None:
        if add_or_remove != 'add' and add_or_remove != 'remove':
            return await self.bot.say("Please specify if I am adding or removing a channel.")

        current_channel_list = ConfigLoader().load_server_config_setting(
            server_id,
            'RoleAssignment',
            'assignment_channel_id'
        )

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
            await ConfigUpdater(self.bot).update_config_file(
                filename,
                'RoleAssignment',
                'assignment_channel_id',
                updated_channel_list.strip()
            )

def setup(bot):
    """This makes it so we can actually use it."""
    bot.add_cog(RoleAssignor(bot))
