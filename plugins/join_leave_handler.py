"""
join_leave_handler.py
@author xNifty
@site https://snoring.ninja

Send a welcome or part message when a user joins or leaves a server.
This is configured on a per server basis.
"""

import random
import discord
import traceback

from resources.config import ConfigLoader
from resources.error_logger import ErrorLogging


class JoinLeaveHandler():
    """
    Functions for welcoming a user or sending a message if
    a user leaves
    """
    def __init__(self, bot):
        self.bot = bot

    async def welcome_user(self, server_id: str, member: str, server: str):
        """
        Send a message to a configured channel when a user joins the server.

        :param server_id: the discord server snowflake ID
        :param member: the discord member snowflake ID
        :param server: the discord server that triggered this
        :return:

        @TODO: can probably reduce arguments and just pass the server argument, and from this grab the server.id
        """
        welcome_enabled = ConfigLoader().load_server_boolean_setting(
            server_id,
            'JoinPart',
            'member_join_enabled'
        )

        if welcome_enabled:
            welcome_channel = ConfigLoader().load_server_config_setting(
                server_id,
                'JoinPart',
                'welcome_channel_id'
            )

            welcome_message = ConfigLoader().load_server_string_setting(
                server_id,
                'JoinPart',
                'welcome_message'
            )

            emote_array = []
            for emoji in member.server.emojis:
                emote_array.append(emoji)

            if not emote_array:
                await self.bot.send_message(
                    discord.Object(id=welcome_channel),
                    welcome_message
                    .replace("{server}", server.name)
                    .replace("{user}", member.mention)
                    .replace("{emote}", ''))
            else:
                await self.bot.send_message(
                    discord.Object(id=welcome_channel),
                    welcome_message
                    .replace("{server}", server.name)
                    .replace("{user}", member.mention)
                    .replace("{emote}", str(random.choice(emote_array))))
        return

    async def on_join_assign_user_role(self, client, server_id: str, member: str):
        """

        :param client: the discord client object
        :param server_id: the discord server snowflake ID
        :param member: discord member object
        :return:
        """
        try:
            welcome_enabled = ConfigLoader().load_server_boolean_setting(
                server_id,
                'JoinPart',
                'assign_role_enabled'
            )

            if welcome_enabled:
                try:
                    join_assignment_role = ConfigLoader().load_server_int_setting(
                        server_id,
                        'JoinPart',
                        'role_assignment_id'
                    )

                    try:
                        if join_assignment_role != '':
                            guild = client.get_server(server_id)
                            for role in guild.roles:
                                # print("{0} - {1}".format(role.id, join_assignment_role))
                                if int(role.id) == join_assignment_role:
                                    # print("join_assignment_role = {0}".format(join_assignment_role))
                                    # print(role)
                                    await self.bot.add_roles(member, role)
                    except Exception as ex2:
                        return await ErrorLogging().log_error(
                            traceback.format_exception(
                                type(ex2),
                                ex2,
                                ex2.__traceback__
                            ),
                            member
                        )
                except Exception as ex:  # update this exception later to be more specific
                    await ErrorLogging().log_error(
                        traceback.format_exception(
                            type(ex),
                            ex,
                            ex.__traceback__
                        ),
                        member
                    )
                    pass
        except Exception as ex:  # update this exception later to be more specific
            await ErrorLogging().log_error(
                traceback.format_exception(
                    type(ex),
                    ex,
                    ex.__traceback__
                ),
                member
            )
            pass
        return

    async def goodbye_user(self, server_id: str, member: str):
        """
        Send a message to a configured channel when a user leaves (or is kicked) from the server.

        :param server_id: the discord server snowflake ID
        :param member: the discord member snowflake ID
        :param server: the discord server that triggered this
        :return:

        @TODO: can probably reduce arguments and just pass the server argument, and from this grab the server.id
        """
        part_enabled = ConfigLoader().load_server_boolean_setting(
            server_id,
            'JoinPart',
            'member_part_enabled'
        )

        if part_enabled:
            part_channel = ConfigLoader().load_server_config_setting(
                server_id,
                'JoinPart',
                'leave_channel_id'
            )

            part_message = ConfigLoader().load_server_string_setting(
                server_id,
                'JoinPart',
                'part_message'
            )
            display_name = member.display_name

            await self.bot.send_message(
                discord.Object(id=part_channel),
                part_message
                .replace("{name}", str(member))
                .replace("{display_name}", display_name)
            )
        return
