"""
join_leave_handler.py
@author xNifty
@site https://snoring.ninja

Send a welcome or part message when a user joins or leaves a server.
This is configured on a per server basis.
"""

import random
import discord

from resources.config import ConfigLoader

class JoinLeaveHandler():
    """
    Functions for welcoming a user or sending a message if
    a user leaves
    """
    def __init__(self, bot):
        self.bot = bot

    async def welcome_user(self, server_id: str, member: str, server: str):
        """Welcome a user to the discord server if enabled"""
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

    async def goodbye_user(self, server_id: str, member: str):
        """Send a message when a user leaves the server."""
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
