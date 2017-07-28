import os
import sys

import pymysql
import sqlite3
from resourcepath import *
from config import ConfigLoader

path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sqlite_database = (os.path.join(path, ConfigLoader().load_config_setting('BotSettings', 'sqlite')))

def selectOneResultParam(query, params):
	try:
		parameters = "("

		for item in params.split():
			parameters = parameters + item + ","

		parameters = parameters + ")"

		print(parameters)

		database = sqlite3.connect(sqlite_database)
		cursor = database.cursor()
		result = cursor.execute(str(query), [parameters])
		print(query)
		print(params)
		print(result.fetchone())
	except Exception as ex:
		print(ex)
	finally:
		try:
			database.close()
			return result.fetchone()
		except Exception as e:
			return

res = selectOneResultParam("SELECT * FROM credit_bet WHERE id=?", 2)
print(res)