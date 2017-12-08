"""
configgenerator.py
@author - xNifty

Functions: Generate the config file for a server
@TODO: generate missing sections and key-values if missing
"""

import os
import configparser

class ConfigGenerator():
    """ConfigGenerator"""
    def __init__(self, bot):
        self.bot = bot
        self.server_settings_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '../channel_settings'
            )
        )

    async def check_if_config_exists(self, server_id):
        """Check if a config file exists.

        :server_id: the Discord ID for the server
        """
        if not os.path.exists(
                '%s.ini' % (
                    os.path.join(
                        self.server_settings_path,
                        str(server_id)
                    )
                )
        ):
            return False
        return True

    async def generate_default_config_file(self, server_id, owner_id):
        """Generate the config file for a server.

        :server_id: the Discord ID for the server
        :owner_id: the Discord ID for the user marked as the server owner
        """
        parser = configparser.ConfigParser()

        # Create each section that we need by default; future cogs
        # may need to handle writing code to modify the config to add sections

        # ServerSettings config['testing'] = {'test': '45', 'test2': 'yes'}
        parser['ServerSettings'] = {
            'owner_id': owner_id,
            'server_id': server_id
        }

        # BotAdmins
        parser['BotAdmins'] = {
            'bot_admin_users': 'NOT_SET',
            'bot_admin_roles': 'NOT_SET'
        }

        # ConfigSettings
        parser['ConfigSettings'] = {
            'not_accepted_channel_id': 'NOT_SET'
        }

        # RoleAssignment
        parser['RoleAssignment'] = {
            'enabled': False,
            'role_list': 'NOT_SET',
            'assignment_channel_id': 'NOT_SET'
        }

        # JoinPart
        parser['JoinPart'] = {
            'member_join_enabled': False,
            'member_part_enabled': False,
            'welcome_channel_id': 'NOT_SET',
            'leave_channel_id': 'NOT_SET',
            'welcome_message': "Welcome to {server}\'s Discord, {user}! Relax and have some fun!",
            'part_message': "{name} ({display_name}) has left the server."
        }

        # BettingGame
        parser['BettingGame'] = {
            'enabled': False,
            'bet_channel_id': 'NOT_SET',
            'minimum_bet': 'NOT_SET'
        }

        # ApiCommands
        parser['ApiCommands'] = {
            'enabled': False,
            'api_channel_id': 'NOT_SET'
        }

        with open(
            '%s.ini' % (
                os.path.join(
                    self.server_settings_path,
                    str(server_id))), 'w'
            ) as configfile:
            parser.write(configfile)
        return await self.bot.say(
            "Configuration file generated. You will need to " \
            "configure the file to your desired settings."
        )
