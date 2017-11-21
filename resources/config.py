"""
config.py
@author - Ryan Malacina (xNifty)

Handls all config based functions that are not used as bot commands
"""

# Imports for ConfigLoader
import os
import configparser
import errno

def get_config_filename(default_filename):
    """Return the filename; probably not needed at this point."""
    return default_filename

def load_config(default_filename):
    """Read in the config file."""
    config = configparser.ConfigParser()
    return config.read(default_filename)

class ConfigLoader():
    """ConfigLoader"""
    def __init__(self, bot=None):
        """Initialize some variables"""
        self.path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
        self.config = load_config('%s.ini' % (os.path.join(self.path, 'niftybot')),)

        self.parser = configparser.ConfigParser()

        self.server_settings_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '../channel_settings')
        )

        self.bot = bot

    def create_directory(self):
        """Create an errors directory if needed."""
        #print "DIRECTORY: %s" % (self.directory,)
        try:
            os.mkdir(self.server_settings_path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    def check_for_bot_config(self):
        """Check if the niftybot.ini file exists
        and if not, create a blank one.

        Returns True or False
        """
        if not self.config:
            print("Generating default niftybot.ini file...")

            parser = configparser.ConfigParser()

            parser.add_section('BotSettings')
            parser.set('BotSettings', 'owner_id', 'NOT_SET')
            parser.set('BotSettings', 'server_id', 'NOT_SET')
            parser.set('BotSettings', 'bot_token', 'NOT_SET')
            parser.set('BotSettings', 'game_name', 'NOT_SET')
            parser.set('BotSettings', 'command_prefix', 'NOT_SET')
            parser.set('BotSettings', 'description', 'NOT_SET')
            parser.set('BotSettings', 'sqlite', 'niftybot.db')
            parser.set('BotSettings', 'enabled_plugins', 'Space separated list ' \
                                '(credit_bet logout api_commands)')
            parser.set('BotSettings', 'error_message', '')
            parser['BotSettings']['error_message'] = 'There was an error with the requested bot ' \
                                'function. Please let the bot owner know to check the error ' \
                                'log for more details.'
            parser.set('BotSettings', 'not_accepted_message', '')
            parser['BotSettings']['not_accepted_message'] = "{0.mention}:\n" \
                                    "I am sorry, you must accept the bot terms of service " \
                                    "to use commands.\n" \
                                    "I may log the following:\n" \
                                    "```Your public discord userID\n" \
                                    "The ID of the server you used in the command\n" \
                                    "Your current display name\n" \
                                    "Information provided to me for different functions, " \
                                    "including but not limited to: GW2 Api Commands, " \
                                    "Credit Betting```\n" \
                                    "Please type {1}accept to accept these terms, which will " \
                                    "expand to allow you to use commands in all servers.\n" \
                                    "If this makes you uncomfortable, please check with " \
                                    "server owners running me to find out what " \
                                    "information they might be logging."


            parser['Debugging'] = {
                'show_db_info': 'false',
                'error_handle_debugger': 'false'
            }

            with open(
                '%s.ini' % (
                    os.path.join(
                        self.path,
                        'niftybot')), 'w'
                ) as configfile:
                parser.write(configfile)
            return False
        return True

    def load_config_setting(self, section, var):
        """Load a config setting from the bot config."""
        self.parser.read(self.config)
        return self.parser.get(section, var)

    def load_config_setting_int(self, section, var):
        """Load int setting from bot config."""
        self.parser.read(self.config)
        return int(self.parser.get(section, var))

    def load_config_setting_string(self, section, var):
        """Load string setting from bot config."""
        self.parser.read(self.config)
        return str(self.parser.get(section, var))

    def load_config_setting_boolean(self, section, var):
        """Load a boolean bot config setting."""
        self.parser.read(self.config)
        return self.parser.getboolean(section, var)

    ####################################################################################
    # Below are for loading specific server config settings, not global config settings
    ####################################################################################
    def load_server_config(self, default_filename):
        """Load a the server config file."""
        config = load_config(
            '%s.ini' % (
                os.path.join(
                    self.server_settings_path,
                    str(default_filename))
            ),
        )
        # honestly, this throws an error in the editor but works fine
        return self.parser.read(config)

    def load_server_config_setting(self, filename, section, var):
        """Load a specific server config side."""
        try:
            loaded_file = load_config(
                '%s.ini' % (
                    os.path.join(
                        self.server_settings_path,
                        str(filename)
                    )
                ),
            )
            self.parser.read(loaded_file)
            return self.parser.get(section, var)
        except configparser.NoSectionError:
            print("Basic config setting missing from server.")

    def load_server_boolean_setting(self, filename, section, var):
        """Load a boolean server config setting."""
        try:
            loaded_file = load_config(
                '%s.ini' % (
                    os.path.join(
                        self.server_settings_path,
                        str(filename)
                    )
                ),
            )
            self.parser.read(loaded_file)
            return self.parser.getboolean(section, var)
        except configparser.NoSectionError:
            print("Boolean section did not exist for server.")

    def load_server_int_setting(self, filename, section, var):
        """Load an int server config setting."""
        try:
            loaded_file = load_config(
                '%s.ini' % (
                    os.path.join(
                        self.server_settings_path,
                        str(filename)
                    )
                ),
            )
            self.parser.read(loaded_file)
            return self.parser.getint(section, var)
        except configparser.NoSectionError:
            print("Integer setting did not exist for server.")

    def load_server_string_setting(self, filename, section, var):
        """Load a string server config setting."""
        try:
            loaded_file = load_config(
                '%s.ini' % (
                    os.path.join(
                        self.server_settings_path,
                        str(filename)
                    )
                ),
            )
            self.parser.read(loaded_file)
            return str(self.parser.get(section, var))
        except configparser.NoSectionError:
            print("String setting did not exist for server.")

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
