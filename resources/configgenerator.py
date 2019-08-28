import os
import configparser


class ConfigGenerator:
    """
    This class handles generating the default configuration file for a server when the server owner uses
    the genconfig command.  Right now, this will only work once and after that it will just do nothing.

    @TODO: allow server owners to use the genconfig whenever they want to add missing section-key-values
    that might be missing, as long as they are defined in this class.

    @TODO: okay, as I looked through code, I think I might have deprecated this class when I combined with the
    config class under resources...yeah, I really should confirm that at some point soon.
    """
    def __init__(self, bot):
        self.bot = bot
        self.server_settings_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '../channel_settings'
            )
        )

    async def check_if_config_exists(self, server_id):
        """
        Check if a config file exists.

        :param server_id: the Discord ID for the server
        :return: True if the file exists, False if it does not
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
        """
        Generate the config file for a server.

        :param server_id: the Discord ID for the server
        :param owner_id: the Discord ID for the user marked as the server owner

        @TODO: with deprecating the ApiCommands, we should probably remove that from ever being set
        """
        parser = configparser.ConfigParser()

        # Create each section that we need by default; future cogs (meaning ones not included by default)
        # will have to handle adding sections to the config file themselves

        parser.add_section('ServerSettings')
        parser.add_section('BotAdmins')
        parser.add_section('ConfigSettings')
        parser.add_section('RoleAssignment')
        parser.add_section('JoinPart')
        parser.add_section('BettingGame')
        parser.add_section('ApiCommands')

        parser.set('ServerSettings', 'owner_id', owner_id)
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
        parser.set('JoinPart', 'role_assignment_id', 'NOT_SET')

        parser.set('BettingGame', 'minimum_bet', '10')
        parser.set('BettingGame', 'enabled', 'false')
        parser.set('BettingGame', 'bet_channel_id', 'NOT_SET')
        parser.set('BettingGame', 'helpme_cooldown', '86400')
        parser.set('BettingGame', 'helpme_minimum', '500')
        parser.set('BettingGame', 'force_multiple', '100')
        parser.set('BettingGame', 'helpme_start_min', '500')
        parser.set('BettingGame', 'helpme_bonus', '100')

        parser.set('ApiCommands', 'enabled', 'false')
        parser.set('ApiCommands', 'api_channel_id', 'NOT_SET')

        with open(
            '%s.ini' % (
                os.path.join(
                    self.server_settings_path,
                    str(server_id))), 'w'
            ) as configfile:
            parser.write(configfile)
        return await self.bot.say(
            "Configuration file generated. You will need to "
            "configure the file to your desired settings."
        )
