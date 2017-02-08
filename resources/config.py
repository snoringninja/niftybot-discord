# Niftybot
# @author - Ryan 'iBeNifty' Malacina
# config.py
# Functions: Set up everything from the config file we use, Load the required config file
# Uses the Twisted IRC Library

############################################

import os
import yaml

NIFTYBOT_CONFIG = 'NIFTYBOT_CONFIG'
DATABASE = 'database'

def get_config_filename(default_filename):
	if NIFTYBOT_CONFIG in os.environ:
		return os.environ[NIFTYBOT_CONFIG]
	return default_filename

def load_config(default_filename):
	with open(get_config_filename(default_filename)) as f:
		return yaml.load(f)