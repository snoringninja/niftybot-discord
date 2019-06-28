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

        parser.add_section('ServerSettings')
        parser.add_section('BotAdmins')
        parser.add_section('ConfigSettings')
        parser.add_section('RoleAssignment')
        parser.add_section('JoinPart')
        parser.add_section('BettingGame')
        parser.add_section('ApiCommands')

        parser.set('ServerSettings', 'owner_id', 'NOT_SET')
        parser.set('ServerSettings', 'server_id', 'NOT_SET')

        parser.set('BotAdmins', 'bot_admin_users', 'NOT_SET')
        parser.set('BotAdmins', 'bot_admin_roles', 'NOT_SET')

        parser.set('ConfigSettings', 'not_accepted_channel_id', 'NOT_SET')

        parser.set('RoleAssignment', 'enabled', 'false')
        parser.set('RoleAssignment', 'role_list', 'NOT_SET')
        parser.set('RoleAssignment', 'assignment_channel_id', 'NOT_SET')

        parser.set('JoinPart', 'member_join_enabled', 'false')
        parser.set('JoinPart', 'member_part_enabled', 'false')
        parser.set('JoinPart', 'welcome_channel_id', 'NOT_SET')
        parser.set('JoinPart', 'leave_channel_id', 'false')
        parser.set('JoinPart', 'welcome_message', 'Welcome to {server}\'s Discord, {user}! Relax and have some fun!')
        parser.set('JoinPart', 'part_message', '{name} ({display_name}) has left the server.')
        parser.set('JoinPart', 'assign_role_enabled', 'false')
        parser.ser('JoinPart', 'role_assignment_id', 'NOT_SET')

        parser.set('BettingGame', 'minimum_bet', '10')
        parser.set('BettingGame', 'enabled', 'false')
        parser.set('BettingGame', 'bet_channel_id', 'NOT_SET')
        parser.set('BettingGame', 'helpme_cooldown', '86400')
        parser.set('BettingGame', 'helpme_minimum', '500')
        parser.set('BettingGame', 'force_multiple', '100')
        parser.set('BettingGame', 'helpme_start_min', '500')
        parser.set('BettingGame', 'helpme_bonus', '100')

        parser.set('ApiCommands', 'welcome_message', 'false')
        parser.set('ApiCommands', 'part_message', 'NOT_SET')


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
