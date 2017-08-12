import discord
import logging
from discord.ext import commands
import random
from datetime import datetime
import string
import time
import traceback

import json
import urllib
from urllib.request import urlopen
import urllib.parse
import urllib.error

from resources.error import error_logging
from resources.config import ConfigLoader
from resources.database import DatabaseHandler

# @TODO : rewrite, cutting down API calls and removing functions.  skills and traits stored in the sqlite db now, so can make far fewer api calls
# @TODO : keep original id building functions, but

class ApiCommands():
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, no_pm=False, name='api')
	@commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
	async def addApiKey(self, ctx, apikey : str, member: discord.Member = None):
		""" Add API key to bot. """
		try:
			member = ctx.message.author
			memberID = ctx.message.author.id
			display_name = ctx.message.author.display_name

			if (ctx.message.channel.is_private == True):
				if member is not None:
					row = DatabaseHandler().fetch_results("SELECT 1 FROM api WHERE discord_id = {0}".format(str(memberID)))

					print(row)

					if row is None:
						base_url = 'https://api.guildwars2.com/v2/tokeninfo?access_token='
						header = {'User-Agent' : 'Mozlla/5.0'}

						permissions = ['account', 'builds', 'characters']

						response_url = base_url + str(apikey)
						header = urllib.parse.urlencode(header)
						header = header.encode("utf-8")
						response = urlopen(response_url)
						response = response.read()
						response = response.decode("utf-8")
						data = json.loads(response)

						granted_permissions = []

						for x in data['permissions']:
							granted_permissions.append(x)

						try:
							for permission in permissions:
								if permission not in granted_permissions:
									return await self.bot.say("Missing required API permission(s). Require account, builds, characters.")
						except Exception as e:
							print("Exception occured; exception:")
							print(e)
							return

						#args = (str(memberID), apikey)
						#print(args)
						query = """INSERT INTO api (discord_id, api_key) VALUES (?, ?)"""
						DatabaseHandler().insertIntoDatabase(query, (str(memberID), apikey))
						return await self.bot.say("{0.mention}, API key added.".format(member))
					else:
						return await self.bot.say("You already have an API key registered.")
				else:
					return await self.bot.say("Some unknown error occured. Please try again.")
			else:
				await self.bot.delete_message(ctx.message)
				return await self.bot.say("{0.mention}: please private message me your API key.".format(member))
		except Exception as e:
			await error_logging().log_error(traceback.format_exc(), 'api_commands: addApiKey', str(member), self.bot)
			print("ERROR! Function: addApiKey. Exception: {0}".format(e))
			return

	def get_character_level(self, api_key, character_name):
		# This function returns character information in the format (exmaple) "Name: Level 80 Charr Mesmer"
		base_url = 'https://api.guildwars2.com/v2/characters/'
		base_url2 = '/core?access_token='
		header = {'User-Agent' : 'Mozlla/5.0'}

		response_url = base_url + str(character_name) + str(base_url2) + str(api_key)
		header = urllib.parse.urlencode(header)
		header = header.encode("utf-8")
		response = urlopen(response_url)
		response = response.read()
		response = response.decode("utf-8")
		data = json.loads(response)

		print(response_url)

		character_name = character_name.replace("%20", " ")

		character_info = ''
		character_info = '{0}: Level {1} {2} {3}'.format(character_name, data['level'], data['race'], data['profession'])

		return character_info

	def get_skill_ids(self, char_name, api_key, game_type):
		#print("get_skill_ids")
		base_url = 'https://api.guildwars2.com/v2/characters/'
		base_url2 = '/skills?access_token='
		header = {'User-Agent' : 'Mozlla/5.0'}

		response_url = base_url + str(char_name) + str(base_url2) + str(api_key)
		header = urllib.parse.urlencode(header)
		header = header.encode("utf-8")
		response = urlopen(response_url)
		response = response.read()
		response = response.decode("utf-8")
		data = json.loads(response)

		print(response_url)

		skill_info = {}

		#print(data)

		for key, value in data['skills'][game_type].items():
			if key != 'pets':
				#print(key)
				#print(value)
				skill_info.update({key:value})

		return skill_info

	def get_skill_data(self, skill_dict):
		#print("get_skill_data")
		id_list = ''
		elite = ''
		heal = ''
		utilities = ''

		# for key, value in skill_dict.items():
		# 	if isinstance(value, list):
		# 		for x in value:
		# 			id_list = id_list + ',' + str(x)
		# 	else:
		# 		id_list = id_list + ',' + str(value)

		# id_list = id_list[1:]

		# base_url_skills = 'https://api.guildwars2.com/v2/skills?ids='
		# response_url_skills = base_url_skills + str(id_list)
		# response_skills = urlopen(response_url_skills)
		# response_skills = response_skills.read()
		# response_skills = response_skills.decode("utf-8")
		# data_skills = json.loads(response_skills)

		# load skills from database
		# elite = DatabaseHandler().fetch_results("SELECT 1 FROM api WHERE discord_id = {0}".format(str(memberID)))

		# for x in range(5):
		# 	if data_skills[x]['slot'] == 'Elite':
		# 		elite = data_skills[x]['name']
		# 		#elite = DatabaseHandler().fetch_results("SELECT 1 FROM api WHERE discord_id = {0}".format(str(memberID)))
		# 	elif data_skills[x]['slot'] == 'Heal':
		# 		heal = data_skills[x]['name']
		# 	elif data_skills[x]['slot'] == 'Utility':
		# 		utilities = utilities + ', ' + str(data_skills[x]['name'])

		elite_id = skill_dict['elite']
		heal_id = skill_dict['heal']
		utilities_list = skill_dict['utilities']

		elite = DatabaseHandler().fetch_results("SELECT skill_name FROM gw2_skills WHERE skill_id = {0}".format(elite_id))
		heal = DatabaseHandler().fetch_results("SELECT skill_name FROM gw2_skills WHERE skill_id = {0}".format(heal_id))

		for x in range(3):
			utility_id = utilities_list[x]
			skill_name = DatabaseHandler().fetch_results("SELECT skill_name FROM gw2_skills WHERE skill_id = {0}".format(utility_id))
			utilities = utilities + ', ' + skill_name[0]

		# trim the leading ", "
		utilities = utilities[2:]

		print(elite[0])
		print(heal[0])
		print(utilities)

		return_string = ("**__Skills__** \n\n"
						"Heal: {0} \n"
						"Utilities: {1} \n"
						"Elite: {2}".format(heal[0], utilities, elite[0]))

		return return_string

	def get_trait_ids(self, char_name, api_key, game_type):
		#print("get_trait_ids")
		base_url = 'https://api.guildwars2.com/v2/characters/'
		base_url2 = '/specializations?access_token='
		header = {'User-Agent' : 'Mozlla/5.0'}

		response_url = base_url + str(char_name) + str(base_url2) + str(api_key)
		header = urllib.parse.urlencode(header)
		header = header.encode("utf-8")
		response = urlopen(response_url)
		response = response.read()
		response = response.decode("utf-8")
		data = json.loads(response)

		trait_info = []

		#print("Len2: {0}".format(len(data['specializations'][game_type])))
		for x in range(len(data['specializations'][game_type])):
			for key, value in data['specializations'][game_type][x].items():
				trait_info.append({key:value})

		#print(trait_info)

		return trait_info

	def get_trait_data(self, trait_dict):
		""" Except not really a dict. """
		#print("get_trait_data")
		trait_list = ''
		trait_spec_list = ''

		trait_list_dict = []
		trait_spec_dict = []

		trait_one = ''
		trait_list_one = ''

		trait_two = ''
		trait_list_two = ''

		trait_three = ''
		trait_list_three = ''

		#print(trait_dict)
		#print(trait_dict[5].items())

		for x in range(len(trait_dict)):
			#print(x)
			for key, value in trait_dict[x].items():
				if isinstance(value, list):
					for x in value:
						trait_list = trait_list + ',' + str(x)
				else:
					trait_spec_list = trait_spec_list + ',' + str(value)

		trait_list = trait_list[1:]
		trait_spec_list = trait_spec_list[1:]

		#print(trait_list)
		#print(trait_spec_list)

		base_url_traits = 'https://api.guildwars2.com/v2/traits?ids='
		response_url_traits = base_url_traits + str(trait_list)
		response_traits = urlopen(response_url_traits)
		response_traits = response_traits.read()
		response_traits = response_traits.decode("utf-8")
		data_traits = json.loads(response_traits)

		base_url_trait_spec = 'https://api.guildwars2.com/v2/specializations?ids='
		response_url_traits_spec = base_url_trait_spec + str(trait_spec_list)
		response_traits_spec = urlopen(response_url_traits_spec)
		response_traits_spec = response_traits_spec.read()
		response_traits_spec = response_traits_spec.decode("utf-8")
		data_traits_spec = json.loads(response_traits_spec)

		for x in range(3):
			trait_id = 0
			trait_name = ''
			#print("Inner: {0}".format(x))
			for key, value in data_traits_spec[x].items():
				if key == 'id':
					trait_id = value
				elif key == 'name':
					trait_name = value
			trait_spec_dict.append({trait_id:trait_name})

		for x in range(9):
			trait_id = 0
			trait_name = ''

			for key, value in data_traits[x].items():
				if key == 'id':
					trait_id = value
				elif key == 'name':
					trait_name = value

			trait_list_dict.append({trait_id:trait_name})

		#print("We're here.")
		for x in range(3):
			for key, value in trait_spec_dict[x].items():
				#print("Another loop: {0}".format(x))
				#print(trait_spec_dict[x].items())
				if x == 0:
					trait_one = value
				elif x == 1:
					trait_two = value
				elif x == 2:
					trait_three = value

		for x in range(9):
			for key, value in trait_list_dict[x].items():
				if (x == 0 or x == 1 or x == 2):
					trait_list_one = trait_list_one + ', ' + value
				if (x == 3 or x == 4 or x == 5):
					trait_list_two = trait_list_two + ', ' + value
				if (x == 6 or x == 7 or x == 8):
					trait_list_three = trait_list_three + ', ' + value

		trait_list_one = trait_list_one[2:]
		trait_list_two = trait_list_two[2:]
		trait_list_three = trait_list_three[2:]

		#print("Spec info: {0}, {1}, {2}".format(trait_one, trait_two, trait_three))
		#print("Trait info: {0}, {1}, {2}".format(trait_list_one, trait_list_two, trait_list_three))

		return_string = ("**__Traits__** \n\n"
						"{0}: {1} \n"
						"{2}: {3} \n"
						"{4}: {5}".format(trait_one, trait_list_one, trait_two, trait_list_two, trait_three, trait_list_three))

		return return_string

	@commands.command(pass_context=True, no_pm=True)
	@commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
	async def build(self, ctx, character_name: str, game_type: str, member: discord.Member = None):
		""" Get PvE, WvW, PvP build info for supplied character. """
		try:
			member = ctx.message.author
			memberID = ctx.message.author.id
			display_name = ctx.message.author.display_name

			print(ctx.message.server.id)
			server_id = str(ctx.message.server.id)

			plugin_list = ConfigLoader().load_server_config_setting(server_id, 'ServerSettings', 'enabled_plugins')
			print("Done! Time to print...")
			print(plugin_list)

			# to make this work, check if the plugin is in the list
			if member is not None and 'api_commands' in plugin_list.split():
				row = DatabaseHandler().fetch_results("""SELECT api_key FROM api WHERE discord_id = {0}""".format(memberID))

				if row is not None:
					try:
						character_name = character_name.replace(" ", "%20")

						returned_skill_ids = self.get_skill_ids(character_name, row[0], game_type)
						returned_char_info = self.get_character_level(row[0], character_name)
						returned_trait_ids = self.get_trait_ids(character_name, row[0], game_type)
						returned_skill_data = self.get_skill_data(returned_skill_ids)
						#returned_trait_data = self.get_trait_data(returned_trait_ids)

						print(returned_char_info)
						print(returned_skill_ids)
						print(returned_trait_ids)
						print(returned_skill_data)

						#return_string = ("{0.mention}: \n"
						#				"```{1}```\n\n"
						#				"{2}\n\n"
						#				"{3}".format(member, returned_char_info, returned_trait_data, returned_skill_data))

						#return await self.bot.say(return_string)
						return
					except urllib.error.HTTPError as e:
						if e.code == 400:
							print("{0}".format(character_name))
							print("{0}".format(game_type))
							print("{0}".format(e))
							await self.bot.say("Character not found.")
						else:
							print("I done failed: {0}.".format(e))
						return
				else:
					return await self.bot.say("{0.mention}, please private message me your API key.".format(member))
			else:
				print("Attempted to use disabled plugin: api_commands")
		except Exception as e:
			print(e)
			return


def setup(bot):
	"""This makes it so we can actually use it."""
	bot.add_cog(ApiCommands(bot))