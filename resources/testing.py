import os
import sys

import sqlite3
from resourcepath import *
from config import ConfigLoader

path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sqlite_database = (os.path.join(path, ConfigLoader().load_config_setting('BotSettings', 'sqlite')))

def selectOneResultParam(query):
	try:

		database = sqlite3.connect(sqlite_database)
		cursor = database.cursor()
		result = cursor.execute(query)
		print(query)
		print(result.fetchone())
	except Exception as ex:
		print(ex)
	finally:
		try:
			database.close()
			return result.fetchone()
		except Exception as e:
			return

res = selectOneResultParam("SELECT * FROM credit_bet WHERE id = {0}".format(2))
print(res)