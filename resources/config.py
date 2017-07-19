# Niftybot
# @author - Ryan 'iBeNifty' Malacina
# config.py
# Functions: Set up everything from the config file we use, Load the required config file

############################################

import os
import yaml

# TODO : I don't think I actually need this
NIFTYBOT_CONFIG = 'NIFTYBOT_CONFIG'
#DATABASE = 'database'
#BOTSETTINGS = 'botsettings'
#DEBUGGING = 'debugging'

def get_config_filename(default_filename):
	if NIFTYBOT_CONFIG in os.environ:
		return os.environ[NIFTYBOT_CONFIG]
	return default_filename

def load_config(default_filename):
	with open(get_config_filename(default_filename)) as f:
		return yaml.load(f)

class ConfigLoader():
	def __init__(self):
		self.path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
		self.config = load_config('%s.yaml' % (os.path.join(self.path, 'niftybot')),)

		self.server_settings_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../channel_settings'))

	def load_config_setting(self, section, var):
		return self.config[section][var]

	# Below are for loading specific server config settings, not global config settings
	def load_server_config(self, default_filename):
		config = load_config('%s.yaml' % (os.path.join(self.server_settings_path, str(default_filename))),)
		return config

	def load_server_config_setting(self, filename, section, var):
		file_settings = self.load_server_config(str(filename))
		return file_settings[section][var]