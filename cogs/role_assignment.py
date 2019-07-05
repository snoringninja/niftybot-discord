"""
role_assignment.py
@author Ryan Malacina (xNifty)
@site https://snoring.ninja
"""

import traceback
import logging
import asyncio

from resources.error_logger import ErrorLogging
from resources.config import ConfigLoader
from resources.bot_resources import BotResources

from cogs.config_commands import ConfigCommands

import discord
from discord.ext import commands


class RoleAssignor:
    """
    Handles commands for adding or removing a role, adding or
    removing a channel, or adding a user to a configured role

    @TODO: allow owners to add roles/channels simply by passing in the
    name of the role or channel instead of requiring them to use the
    snowflake ID; if there happens to be more than one of either, then
    require the owner to use the specific ID
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=False, name='guild')
    @commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
    @asyncio.coroutine
    def assign_role(self, ctx, *, guild: str, member: discord.Member = None):
        """
        Assign users to configured roles if requested.  Command is executed via the `guild` command.

        Examples:
            > guild Test
            {user.mention}: You've been successfully added to {guild_name}.

            > guild Test
            {user.mention}: You've been removed from {guild_name}.

        :param ctx: discord.py Context
        :param guild: the requested group name, uses consume rest behavior
        :param member: optional discord.Member object
        :return: Nothing
        """
        server_id = ctx.message.server.id

        if member is None:
            member = ctx.message.author

        plugin_enabled = ConfigLoader().load_server_boolean_setting(
            server_id,
            'RoleAssignment',
            'enabled'
        )

        if member is not None and plugin_enabled:
            requested_guild = discord.utils.get(ctx.message.server.roles, name=guild)

            if requested_guild is None:
                # We ran into an issue where a role name was using acute accents
                # This is the attempt to fix that if requested_guild is none
                # If still none after this we'll need to get examples to fix it
                guild = guild.replace("'", "’")
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
                yield from self.bot.say("This plugin is not configured for this server.")
                return

            channel_list = []
            for channel in map(int, assignment_channel_list.split()):
                channel_list.append(channel)

            if requested_guild is not None:

                role_list_split = []
                for role in map(int, role_list.split()):
                    role_list_split.append(role)

                if int(ctx.message.channel.id) in channel_list and \
                        int(requested_guild.id) in role_list_split:
                    for role in ctx.message.author.roles:
                        if role.id == requested_guild.id:
                            yield from self.bot.remove_roles(
                                ctx.message.author, requested_guild)
                            yield from self.bot.send_message(
                                ctx.message.channel,
                                "{0.mention}: You've been removed from {1}."
                                .format(member, requested_guild.name)
                            )
                            return

                    # So we got this far, add the user to the role
                    yield from self.bot.add_roles(ctx.message.author, requested_guild)
                    yield from self.bot.send_message(
                        ctx.message.channel,
                        "{0.mention}: You've been successfully "
                        "added to {1}!".format(member, requested_guild.name))
                    return
        return

    @commands.command(pass_context=True, no_pm=False, name='role')
    @commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
    async def update_role_list(self, ctx, add_or_remove: str,
                               role_id: str, member: discord.Member = None
                               ):
        """
        Update the configured role list to add or remove a group. Command is executed via the `role` command.

        Examples:
            > role add Test
            Configuration file updated.

            > role add Test
            Role already added.

            > role test Test
            Please specify if I am adding or removing a role.

            > role remove Test
            Configuration file updated.

        :param ctx: discord.py Context
        :param add_or_remove: (str) [add, remove] passed in string to determine if a role is being added or removed
        :param role_id: discord snowflake ID for the role, can be added via direct pinging of the role
        :param member: optional discord.Member object
        :return:
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

            # Somewhat ugly fix for when mentioning the role to strip stuff out
            role_id = role_id.replace('<@&', '')
            role_id = role_id.replace('>', '')
            role_id = role_id.strip()

            updated_role_list = ''

            if add_or_remove == 'add':
                if not BotResources().contains_word(current_role_list, role_id):
                    if current_role_list == 'NOT_SET':
                        updated_role_list = role_id
                    else:
                        updated_role_list = current_role_list + " " + role_id
                else:
                    return await self.bot.say("Role already added.")

            if add_or_remove == 'remove':
                if BotResources().contains_word(current_role_list, role_id):
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
    async def update_channel_list(self, ctx, add_or_remove: str,
                                  channel_id: str, member: discord.Member = None
                                  ):
        """
        Update the configured channel list to add or remove a channel where the guild command can be used.
        Command is executed via the `rolechannel` command.

        Examples:
            > rolechannel add 1234567890
            Configuration file updated.

            > rolechannel add 1234567890
            Role already added.
            
            > rolechannel test 1234567890
            Please specify if I am adding or removing a channel.

            > rolechannel remove 1234567890
            Configuration file updated.

        :param ctx: discord.py Context
        :param add_or_remove: (str) [add, remove] passed in string to determine if a channel is being added or removed
        :param channel_id: discord snowflake ID for the channel, requires the direct ID and cannot be added via pinging
        :param member: optional discord.Member object
        :return:
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
                if not BotResources().contains_word(current_channel_list, channel_id):
                    if current_channel_list == 'NOT_SET':
                        updated_channel_list = channel_id
                    else:
                        updated_channel_list = current_channel_list + " " + channel_id
                else:
                    return await self.bot.say("Channel already added.")

                if add_or_remove == 'remove':
                    if BotResources().contains_word(current_channel_list, channel_id):
                        updated_channel_list = current_channel_list.strip(' ' + channel_id + ' ')

                if updated_channel_list.isspace() or len(updated_channel_list) == 0:
                    updated_channel_list = 'NOT_SET'

                filename = ctx.message.server.id
                await ConfigCommands(self.bot).update_config_file(
                    filename,
                    'RoleAssignment',
                    'assignment_channel_id',
                    updated_channel_list.strip(),
                    ctx.message
                )


def setup(bot):
    """This makes it so we can actually use it."""
    bot.add_cog(RoleAssignor(bot))
