"""
config.py
@author - Ryan Malacina (xNifty)

Functions: Set up everything from the config file we use, Load the required config file
"""

# Imports for ConfigLoader
import os
import configparser

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
        return self.parser.read(config)

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
