"""
config.py
@author - Ryan Malacina (xNifty)

Functions: Set up everything from the config file we use, Load the required config file
"""

# Imports for ConfigLoader
import os
import configparser
import traceback

def get_config_filename(default_filename):
    """Return the filename; probably not needed at this point."""
    return default_filename

def load_config(default_filename):
    """Read in the config file."""
    config = configparser.ConfigParser()
    return config.read(default_filename)

class ConfigLoader():
    """ConfigLoader"""
    def __init__(self):
        """Initialize some variables"""
        self.path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
        self.config = load_config('%s.ini' % (os.path.join(self.path, 'niftybot')),)

        self.parser = configparser.ConfigParser()

        self.server_settings_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '../channel_settings')
        )

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
        return config.read()

    def load_server_config_setting(self, filename, section, var):
        """Load a specific server config side."""
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

    def load_server_config_setting_boolean(self, filename, section, var):
        """Load a boolean server config setting."""
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

    def load_server_config_setting_int(self, filename, section, var):
        """Load an int server config setting."""
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

    def load_server_config_setting_string(self, filename, section, var):
        """Load a string server config setting."""
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

# We have to import this error since this is a combined file as
# of now. Eventually move ConfigGenerator to its own file
from resources.error import ErrorLogging

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
