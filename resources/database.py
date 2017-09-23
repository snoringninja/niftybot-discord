# Niftybot
# @author - Ryan 'iBeNifty' Malacina
# database.py
# Functions: Handle the SQLite stuff
############################################

import os
import sys

import sqlite3
from resources.resourcepath import *
from resources.config import ConfigLoader

class DatabaseHandler(object):
	# @TODO : need a database generation script
	# @TODO : close connection
	# @TODO : NEED TO USE PARAMATIZED QUERIES EVERY TIME

	def __init__(self):
		self.path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
		self.sqlite_database = (os.path.join(self.path, ConfigLoader().load_config_setting('BotSettings', 'sqlite')))

	def connected_to_sqlite(self):
		connected = False
		print(self.sqlite_database)
		try:
			connection = sqlite3.connect(self.sqlite_database)
			connected = True
		except Exception as e:
			print(e)
		finally:
			if connected == True:
				connection.close()
			print("Connection status: {0}".format(connected))
			return

	def fetch_results(self, query):
		try:
			database = sqlite3.connect(self.sqlite_database)
			cursor = database.cursor()
			executed = cursor.execute(query)
			result = executed.fetchone()
			database.close()
		except Exception as ex:
			print(ex)
			print("Database fetch_results error.")
		finally:
			try:
				return result
			except Exception as e:
				print(e)
				return

	def fetch_all_results(self, query):
		try:
			database = sqlite3.connect(self.sqlite_database, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
			cursor = database.cursor()
			executed = cursor.execute(query)
			result = executed.fetchall()
			database.close()
		except Exception as ex:
			print(ex)
			print("Database fetch_all_results error.")
		finally:
			try:
				return result
			except Exception as e:
				print(e)
				return	

	def update_database(self, query):
		try:
			database = sqlite3.connect(self.sqlite_database, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
			cursor = database.cursor()
			executed = cursor.execute(query)
			database.commit()
			database.close()
		except Exception as e:
			print("update_database error: {0}.".format(e))
			return

	def update_database_with_args(self, query, args):
		try:
			database = sqlite3.connect(self.sqlite_database, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
			cursor = database.cursor()
			executed = cursor.execute(query, args)
			database.commit()
			database.close()
		except Exception as e:
			print("update_database error: {0}.".format(e))
			return

	def insert_into_database(self, query, params):
		try:
			database = sqlite3.connect(self.sqlite_database, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
			cursor = database.cursor()
			result = cursor.execute(query, params)
			database.commit()
			new_row = result.fetchone()
			database.close()
		except Exception as ex:
			print(ex)
		finally:
			try:
				return new_row
			except Exception as e:
				return
