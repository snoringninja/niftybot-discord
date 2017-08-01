# Niftybot
# @author - Ryan 'iBeNifty' Malacina
# config.py
# Functions: Set up everything from the config file we use, Load the required config file

############################################

import os
import yaml

import configparser

# TODO : I don't think I actually need this
#NIFTYBOT_CONFIG = 'NIFTYBOT_CONFIG'
#DATABASE = 'database'
#BOTSETTINGS = 'botsettings'
#DEBUGGING = 'debugging'

def get_config_filename(default_filename):
	# if NIFTYBOT_CONFIG in os.environ:
	# 	return os.environ[NIFTYBOT_CONFIG]
	return default_filename

def load_config(default_filename):
	#with open(get_config_filename(default_filename)) as f:
		#return yaml.load(f)
	config = configparser.ConfigParser()
	return config.read(default_filename)

class ConfigLoader():
	def __init__(self):
		self.path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../'))
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
		return int(self.parser.get(section, var))

	def load_server_config_setting_string(self, filename, section, var):
		parser = configparser.ConfigParser()
		loaded_file = load_config('%s.ini' % (os.path.join(self.server_settings_path, str(filename))),)
		self.parser.read(loaded_file)
		return str(self.parser.get(section, var))