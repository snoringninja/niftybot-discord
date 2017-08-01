import pymysql
import sqlite3
from resourcepath import *
from config import ConfigLoader

import json
import urllib
from urllib.request import urlopen
import urllib.parse
import urllib.error
import time

id_list = []

path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../'))
sqlite_database = (os.path.join(path, ConfigLoader().load_config_setting('BotSettings', 'sqlite')))

# some variables
dump_skills = 1

print(sqlite_database)

database = sqlite3.connect(sqlite_database)
cursor = database.cursor()

base_url_skills = 'https://api.guildwars2.com/v2/skills'
response_url_skills = base_url_skills
response_skills = urlopen(response_url_skills)
response_skills = response_skills.read()
response_skills = response_skills.decode("utf-8")
data_skills = json.loads(response_skills)

#print(data_skills)

def build_id_list(start_int, end_int):
	cur_string = ""
	print(start_int, end_int)
	for x in range(start_int, end_int + 1):
		cur_id = data_skills[x]
		cur_string = cur_string + str(data_skills[x]) + ', '

	cur_string = cur_string.replace(' ', '%20')
	return cur_string

def insert_into_db(id_list):
	for x in range(len(id_list)):
		try:
			slot = ""
			slot = id_list[x]['slot']
		except Exception as ex:
			slot = "EMPTY_SLOT"
		cursor.execute("INSERT INTO gw2_skills (skill_id, skill_name, slot) VALUES (?, ?, ?)", (id_list[x]['id'], id_list[x]['name'], slot))
		database.commit()

# for y in range(len(data_skills2)):
# 	print("{0}, {1}".format(data_skills2[y]['id'], data_skills2[y]['name']))

#print("Loop one complete.")

counter = 0
start_int = 0

if dump_skills == 1:
	for x in range(19):
		print(x)
		if x <= 17:
			end_int = (counter + 1) * 100
			counter = counter + 1

			id_list = []
			id_list = build_id_list(start_int, end_int)

			data_skills2 = []
			base_url_skills2 = 'https://api.guildwars2.com/v2/skills?ids=' + str(id_list)
			response_url_skills2 = base_url_skills2
			response_skills2 = urlopen(response_url_skills2)
			response_skills2 = response_skills2.read()
			response_skills2 = response_skills2.decode("utf-8")
			data_skills2 = json.loads(response_skills2)

			insert_into_db(data_skills2)

			start_int = end_int + 1

			time.sleep(10)
		elif x == 18:
			#id_list = []
			#id_list = build_id_list(1802, 1863)

			data_skills2 = []
			base_url_skills2 = 'https://api.guildwars2.com/v2/skills?ids=39646,%2039648,%2039653,%2039664,%2039667,%2039668,%2039673,%2039674,%2039684,%2039685,%2039686,%2039691,%2039694,%2039701,%2039708,%2039711,%2039713,%2039714,%2039728,%2039734,%2039745,%2039746,%2039748,%2039755,%2039760,%2039765,%2039770,%2039775,%2039782,%2039787,%2039788,%2039790,%2039795,%2039801,%2039816,%2039823,%2039829,%2039830,%2039839,%2039845,%2039847,%2039848,%2039849,%2039853,%2039854,%2039857,%2039863,%2039867,%2039874,%2039875,%2039879,%2039884,%2039886,%2039889,%2039894,%2039895,%2039910,%2039911,%2039915,%2039916,%2039920,%2039924'
			response_url_skills2 = base_url_skills2
			response_skills2 = urlopen(response_url_skills2)
			response_skills2 = response_skills2.read()
			response_skills2 = response_skills2.decode("utf-8")
			data_skills2 = json.loads(response_skills2)

			insert_into_db(data_skills2)

# data_skills2 = []
# base_url_skills2 = 'https://api.guildwars2.com/v2/skills?ids=39646,%2039648,%2039653,%2039664,%2039667,%2039668,%2039673,%2039674,%2039684,%2039685,%2039686,%2039691,%2039694,%2039701,%2039708,%2039711,%2039713,%2039714,%2039728,%2039734,%2039745,%2039746,%2039748,%2039755,%2039760,%2039765,%2039770,%2039775,%2039782,%2039787,%2039788,%2039790,%2039795,%2039801,%2039816,%2039823,%2039829,%2039830,%2039839,%2039845,%2039847,%2039848,%2039849,%2039853,%2039854,%2039857,%2039863,%2039867,%2039874,%2039875,%2039879,%2039884,%2039886,%2039889,%2039894,%2039895,%2039910,%2039911,%2039915,%2039916,%2039920,%2039924'
# response_url_skills2 = base_url_skills2
# response_skills2 = urlopen(response_url_skills2)
# response_skills2 = response_skills2.read()
# response_skills2 = response_skills2.decode("utf-8")
# data_skills2 = json.loads(response_skills2)

# insert_into_db(data_skills2)

# x = build_id_list(401, 500)
# print(x)