"""
configgenerator.py
@author - Ryan Malacina (xNifty)

Functions: Generate the config file for a server
@TODO: generate missing sections and key-values if missing
"""

import os
import traceback
import configparser

from resources.error_logger import ErrorLogging

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
        """Check if a config file exists."""
        try:
            if not os.path.exists('%s.ini' % (os.path.join(
                    self.server_settings_path,
                    str(server_id)))):
                return False
            return True
        except Exception:
            await ErrorLogging().log_error(
                traceback.format_exc(),
                'ConfigGenerator: checkIfConfigExists'
            )
            return True

    async def generate_default_config_file(self, server_id, owner_id):
        """Generate the config file for a server."""
        parser = configparser.ConfigParser()

        # Create each section that we need by default; future cogs
        # may need to handle writing code to modify the config to add sections

        # ServerSettings config['testing'] = {'test': '45', 'test2': 'yes'}
        parser['ServerSettings'] = {
            'owner_id': owner_id,
            'server_id': server_id,
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
            'leave_channel_id': 'NOT_SET'
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


        try:
            with open('%s.ini' % (
                os.path.join(
                    self.server_settings_path,
                    str(server_id))), 'w'
                     ) as configfile:
                parser.write(configfile)
                return await self.bot.say(
                    "Configuration file generated. You will need to \
                    configure the file to your required settings.")
        except Exception:
            await ErrorLogging().log_error(
                traceback.format_exc(),
                'ConfigGenerator: checkIfConfigExists'
            )
            return await self.bot.say(
                "Error generating configuration file: {0}"
                .format(traceback.format_exc())
            )
