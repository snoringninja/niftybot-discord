# Niftybot
# @author - Ryan Malacina (xNifty)
# config.py
# Functions: Set up everything from the config file we use, Load the required config file

############################################

# Imports for ConfigLoader
import os
import configparser

# Needed for ConfigGenerator
import discord
import traceback

def get_config_filename(default_filename):
    return default_filename

def load_config(default_filename):
    config = configparser.ConfigParser()
    return config.read(default_filename)

class ConfigLoader():
    def __init__(self):
        self.path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
        self.config = load_config('%s.ini' % (os.path.join(self.path, 'niftybot')),)

        self.parser = configparser.ConfigParser()

        self.server_settings_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../channel_settings'))

    def load_config_setting(self, section, var):
        self.parser.read(self.config)
        return self.parser.get(section, var)

    def load_config_setting_int(self, section, var):
        self.parser.read(self.config)
        return int(self.parser.get(section, var))

    def load_config_setting_string(self, section, var):
        self.parser.read(self.config)
        return str(self.parser.get(section, var))

    ####################################################################################
    # Below are for loading specific server config settings, not global config settings
    ####################################################################################
    def load_server_config(self, default_filename):
        config = load_config('%s.ini' % (os.path.join(self.server_settings_path, str(default_filename))),)
        return config.read()

    def load_server_config_setting(self, filename, section, var):
        parser = configparser.ConfigParser()
        loaded_file = load_config('%s.ini' % (os.path.join(self.server_settings_path, str(filename))),)
        self.parser.read(loaded_file)
        return self.parser.get(section, var)

    def load_server_config_setting_boolean(self, filename, section, var):
        parser = configparser.ConfigParser()
        loaded_file = load_config('%s.ini' % (os.path.join(self.server_settings_path, str(filename))),)
        self.parser.read(loaded_file)
        return self.parser.getboolean(section, var)

    def load_server_config_setting_int(self, filename, section, var):
        parser = configparser.ConfigParser()
        loaded_file = load_config('%s.ini' % (os.path.join(self.server_settings_path, str(filename))),)
        self.parser.read(loaded_file)
        return self.parser.getint(section, var)

    def load_server_config_setting_string(self, filename, section, var):
        parser = configparser.ConfigParser()
        loaded_file = load_config('%s.ini' % (os.path.join(self.server_settings_path, str(filename))),)
        self.parser.read(loaded_file)
        return str(self.parser.get(section, var))

from resources.error import error_logging

class ConfigGenerator():
    def __init__(self, bot):
        self.bot = bot
        self.server_settings_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../channel_settings'))

    async def checkIfConfigExists(self, server_id):
        try:
            if not os.path.exists('%s.ini' % (os.path.join(self.server_settings_path, str(server_id)))):
                return False
            else:
                return True
        except Exception as e:
            await error_logging().log_error(traceback.format_exc(), 'ConfigGenerator: checkIfConfigExists')
            print(e)
            return True

    async def generateDefaultConfigFile(self, server_id, owner_id):
        parser = configparser.ConfigParser()

        # Create each section that we need by default; future cogs may need to handle writing code to modify the config to add sections

        # ServerSettings config['testing'] = {'test': '45', 'test2': 'yes'}
        parser['ServerSettings'] = {'owner_id': owner_id, 'server_id': server_id, 'not_accepted_channel_id': 'NOT_SET'}

        # RoleAssignment
        parser['RoleAssignment'] = {'enabled': False, 'role_list': 'NOT_SET', 'assignment_channel_id': 'NOT_SET'}

        # JoinPart
        parser['JoinPart'] = {'member_join_enabled': False, 'member_part_enabled': False, 'welcome_channel_id': 'NOT_SET', 'leave_channel_id': 'NOT_SET'}

        # BettingGame
        parser['BettingGame'] = {'enabled': False, 'bet_channel_id': 'NOT_SET', 'minimum_bet': 'NOT_SET'}

        # ApiCommands
        parser['ApiCommands'] = {'enabled': False, 'api_channel_id': 'NOT_SET'}


        try:
            with open('%s.ini' % (os.path.join(self.server_settings_path, str(server_id))), 'w') as configfile:
                parser.write(configfile)
                return await self.bot.say("Configuration file generated. You will need to configure the file to your required settings.")
        except Exception as e:
            await error_logging().log_error(traceback.format_exc(), 'ConfigGenerator: checkIfConfigExists')
            print(e)
            return await self.bot.say("Error generating configuration file: {0}".format(traceback.format_exc()))