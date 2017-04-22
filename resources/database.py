# Niftybot
# @author - Ryan 'iBeNifty' Malacina
# database.py
# Functions: Handle the MySQL DB connection
# Uses the Twisted IRC Library

############################################

import os
import sys

import pymysql
from resources.resourcepath import *
from resources.config import DATABASE, load_config

class DatabaseHandler(object):
	# TODO : comment this shit so we know what everything does
	_db_connection = None
	_db_cur = None

	def __init__(self):
		self.path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
		self.config = load_config('%s.yaml' % (os.path.join(self.path, 'niftybot')),)
		self.host = self.config[DATABASE]['host']
		self.user = self.config[DATABASE]['username']
		self.password = self.config[DATABASE]['password']
		self.database = self.config[DATABASE]['database']

		self._db_connection = pymysql.connect(self.host, 
		self.user, 
		self.password, 
		self.database)

		self._db_cur = self._db_connection.cursor()
		self._db_curdict = self._db_connection.cursor(pymysql.cursors.DictCursor)
		self._db_connection.ping()

	def query(self, query, params):
		return self._db_cur.execute(query, params)

	def fetchresult(self, query, params):
		cursor = self._db_cur.execute(query, params)
		return self._db_cur.fetchone()

	def manipulateDB(self, query, params):
		self._db_cur.execute(query, params)
		return self._db_connection.commit()

	def selectOnly(self, query):
		return self._db_cur.execute(query)

	def selectAllOptions(self, query):
		self._db_cur.execute(query)
		return self._db_cur.fetchall()

	def selectAllOptionsParams(self, query, params):
		self._db_cur.execute(query, params)
		return self._db_cur.fetchall()

	def selectAllOptionsDict(self, query):
		#print(query)
		self._db_curdict.execute(query)
		return self._db_curdict.fetchall()

	def executeStoredProcedureCommit(self, query, params):
		#print(query)
		#print(params)
		self._db_cur.callproc(query, params)
		return self._db_connection.commit()

	def executeStoredProcedure(self, query, params):
		#print(query)
		#print(params)
		self._db_cur.callproc(query, params)
		return self._db_cur.fetchall()

	def __del__(self):
		self._db_connection.close()

	def attemptConnection(self):
		if self._db_cur.execute("""SELECT 1 FROM `users`"""):
			return True
		else:
			return False

	def get_conn_details(self):
		"""DEBUG COMMAND; REMOVE BEFORE RELEASE"""
		print(self.host, self.user, self.password, self.database)
		return