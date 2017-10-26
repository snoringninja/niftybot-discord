"""
api_commands.py
@author Ryan 'iBeNifty' Malacina
@site https://snoring.ninja
"""

import json
import urllib
from urllib.request import urlopen
import urllib.parse
import urllib.error
import traceback

import discord
from discord.ext import commands

from resources.error import ErrorLogging
from resources.config import ConfigLoader
from resources.database import DatabaseHandler


class ApiCommands():
    """Multiple commands based around the Guild Wars 2 API."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=False, name='api')
    @commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
    async def add_api_key(self, ctx, apikey: str, member: discord.Member=None):
        """ Add API key to bot. """
        try:
            member = ctx.message.author
            member_id = ctx.message.author.id

            if ctx.message.channel.is_private:
                if member is not None:
                    row = DatabaseHandler().fetch_results(
                        "SELECT 1 FROM api WHERE discord_id = {0}".format(str(member_id)))

                    if row is None:
                        base_url = 'https://api.guildwars2.com/v2/tokeninfo?access_token='
                        header = {'User-Agent': 'Mozlla/5.0'}

                        permissions = ['account', 'builds', 'characters']

                        response_url = base_url + str(apikey)
                        header = urllib.parse.urlencode(header)
                        header = header.encode("utf-8")
                        response = urlopen(response_url)
                        response = response.read()
                        response = response.decode("utf-8")
                        data = json.loads(response)

                        granted_permissions = []

                        for value in data['permissions']:
                            granted_permissions.append(value)

                        try:
                            for permission in permissions:
                                if permission not in granted_permissions:
                                    return await self.bot.say(
                                        "Missing required API permission(s). \
                                        Require account, builds, characters."
                                    )
                        except Exception:
                            print("Exception occured; exception:")
                            return

                        query = """INSERT INTO api (discord_id, api_key) VALUES (?, ?)"""
                        DatabaseHandler().insert_into_database(query, (str(member_id), apikey))
                        return await self.bot.say("{0.mention}, API key added.".format(member))
                    else:
                        return await self.bot.say("You already have an API key registered.")
                else:
                    return await self.bot.say("Some unknown error occured. Please try again.")
            else:
                await self.bot.delete_message(ctx.message)
                return await self.bot.say(
                    "{0.mention}: please private message me your API key."
                    .format(member)
                )
        except Exception:
            await ErrorLogging().log_error(
                traceback.format_exc(),
                'api_commands: addApiKey',
                str(member),
                self.bot
            )
            return

    async def get_character_level(self, api_key, character_name):
        """
        This function returns character information in the format
        (exmaple) "Name: Level 80 Charr Mesmer"
        """
        try:
            base_url = 'https://api.guildwars2.com/v2/characters/'
            base_url2 = '/core?access_token='
            header = {'User-Agent': 'Mozlla/5.0'}

            response_url = base_url + \
                str(character_name) + str(base_url2) + str(api_key)
            header = urllib.parse.urlencode(header)
            header = header.encode("utf-8")
            response = urlopen(response_url)
            response = response.read()
            response = response.decode("utf-8")
            data = json.loads(response)

            character_name = character_name.replace("%20", " ")

            character_info = ''
            character_info = '{0}: Level {1} {2} {3}'.format(
                character_name, data['level'], data['race'], data['profession']
            )

            return character_info
        except Exception:
            await ErrorLogging().log_error(
                traceback.format_exc(),
                'api_commands: get_character_level',
                "",
                self.bot
            )

    async def get_skill_ids(self, char_name, api_key, game_type):
        """Get the list of skill IDs"""
        try:
            base_url = 'https://api.guildwars2.com/v2/characters/'
            base_url2 = '/skills?access_token='
            header = {'User-Agent': 'Mozlla/5.0'}

            response_url = base_url + \
                str(char_name) + str(base_url2) + str(api_key)
            header = urllib.parse.urlencode(header)
            header = header.encode("utf-8")
            response = urlopen(response_url)
            response = response.read()
            response = response.decode("utf-8")
            data = json.loads(response)

            skill_info = {}

            for key, value in data['skills'][game_type].items():
                if key != 'pets':
                    skill_info.update({key: value})

            return skill_info
        except Exception:
            await ErrorLogging().log_error(
                traceback.format_exc(),
                'api_commands: get_skill_ids',
                "",
                self.bot
            )

    async def get_skill_data(self, skill_dict):
        """Gather the skill data names from the database."""
        try:
            elite = ''
            heal = ''
            utilities = ''

            elite_id = skill_dict['elite']
            heal_id = skill_dict['heal']
            utilities_list = skill_dict['utilities']

            elite = DatabaseHandler().fetch_results(
                "SELECT skill_name FROM gw2_skills WHERE skill_id = {0}".format(elite_id))
            heal = DatabaseHandler().fetch_results(
                "SELECT skill_name FROM gw2_skills WHERE skill_id = {0}".format(heal_id))

            for key in range(3):
                utility_id = utilities_list[key]
                skill_name = DatabaseHandler().fetch_results(
                    "SELECT skill_name FROM gw2_skills WHERE skill_id = {0}".format(
                        utility_id)
                )
                utilities = utilities + ', ' + skill_name[0]

            # trim the leading ", "
            utilities = utilities[2:]

            return_string = (
                "**__Skills__** \n\n"
                "Heal: {0} \n"
                "Utilities: {1} \n"
                "Elite: {2}".format(heal[0], utilities, elite[0])
            )

            return return_string
        except Exception:
            await ErrorLogging().log_error(
                traceback.format_exc(),
                'api_commands: get_skill_data',
                "",
                self.bot
            )

    async def get_trait_ids(self, char_name, api_key, game_type):
        """Get the list of trait IDs"""
        base_url = 'https://api.guildwars2.com/v2/characters/'
        base_url2 = '/specializations?access_token='
        header = {'User-Agent': 'Mozlla/5.0'}

        response_url = base_url + \
            str(char_name) + str(base_url2) + str(api_key)
        header = urllib.parse.urlencode(header)
        header = header.encode("utf-8")
        response = urlopen(response_url)
        response = response.read()
        response = response.decode("utf-8")
        data = json.loads(response)

        trait_info = []

        for item in range(len(data['specializations'][game_type])):
            for key, value in data['specializations'][game_type][item].items():
                trait_info.append({key: value})

        return trait_info

    async def get_trait_data(self, trait_dict):
        """ Except not really a dict. """
        trait_list = []
        trait_spec_list = []

        trait_one = ''
        trait_list_one = ''

        trait_two = ''
        trait_list_two = ''

        trait_three = ''
        trait_list_three = ''

        for item in range(len(trait_dict)):
            for value in trait_dict[item].items():
                if isinstance(value, list):
                    for key in value:
                        trait_list.append(key)
                else:
                    trait_spec_list.append(value)

        print(trait_spec_list)
        trait_one = DatabaseHandler().fetch_results(
            "SELECT spec_name FROM gw2_specs WHERE spec_id = {0}".format(int(trait_spec_list[0])))
        trait_two = DatabaseHandler().fetch_results(
            "SELECT spec_name FROM gw2_specs WHERE spec_id = {0}".format(int(trait_spec_list[1])))
        trait_three = DatabaseHandler().fetch_results(
            "SELECT spec_name FROM gw2_specs WHERE spec_id = {0}".format(int(trait_spec_list[2])))

        for item in range(9):
            spec_name = DatabaseHandler().fetch_results(
                "SELECT trait_name FROM gw2_traits WHERE trait_id = {0}"
                .format(int(trait_list[item]))
            )
            if item in range(3):
                trait_list_one = trait_list_one + ', ' + spec_name[0]
            elif item in range(3, 6):
                trait_list_two = trait_list_two + ', ' + spec_name[0]
            else:
                trait_list_three = trait_list_three + ', ' + spec_name[0]

        trait_list_one = trait_list_one[2:]
        trait_list_two = trait_list_two[2:]
        trait_list_three = trait_list_three[2:]

        return_string = (
            "**__Traits__** \n\n"
            "{0}: {1} \n"
            "{2}: {3} \n"
            "{4}: {5}".format(
                trait_one[0],
                trait_list_one,
                trait_two[0],
                trait_list_two,
                trait_three[0],
                trait_list_three))

        return return_string

    @commands.command(pass_context=True, no_pm=True)
    @commands.cooldown(rate=1, per=30, type=commands.BucketType.server)
    async def build(self, ctx, game_type: str, *, character_name: str, member: discord.Member=None):
        """ Get PvE, WvW, PvP build info for supplied character. """
        try:
            member = ctx.message.author
            member_id = ctx.message.author.id

            server_id = str(ctx.message.server.id)

            plugin_enabled = ConfigLoader().load_server_boolean_setting(
                server_id, 'ApiCommands', 'enabled')

            # to make this work, check if the plugin is in the list
            if member is not None and plugin_enabled:
                row = DatabaseHandler().fetch_results(
                    """SELECT api_key FROM api WHERE discord_id = {0}""".format(member_id))

                if row is not None:
                    try:
                        character_name = character_name.replace(" ", "%20")

                        returned_skill_ids = await self.get_skill_ids(
                            character_name,
                            row[0],
                            game_type
                        )

                        returned_char_info = await self.get_character_level(
                            row[0],
                            character_name
                        )

                        returned_trait_ids = await self.get_trait_ids(
                            character_name,
                            row[0],
                            game_type
                        )

                        returned_skill_data = await self.get_skill_data(
                            returned_skill_ids
                        )
                        returned_trait_data = await self.get_trait_data(
                            returned_trait_ids
                        )

                        return_string = ("{0.mention}: \n" "```{1}```\n\n" "{2}\n\n" "{3}".format(
                            member, returned_char_info, returned_trait_data, returned_skill_data))

                        return await self.bot.say(return_string)
                    except urllib.error.HTTPError as error_code:
                        if error_code.code == 400:
                            print("{0}".format(character_name))
                            print("{0}".format(game_type))
                            print("{0}".format(error_code))
                            await self.bot.say("Character not found.")
                        else:
                            print("I done failed: {0}.".format(error_code))
                        return
                else:
                    return await self.bot.say(
                        "{0.mention}, please private message me your API key."
                        .format(member)
                    )
            else:
                print("Attempted to use disabled plugin: api_commands")
        except Exception:
            return await ErrorLogging().log_error(
                traceback.format_exc(),
                'api_commands: build',
                str(member),
                self.bot
            )


def setup(bot):
    """This makes it so we can actually use it."""
    bot.add_cog(ApiCommands(bot))
