"""
api_commands.py
@author xNifty
@site https://snoring.ninja

Return information based on the GW2 API
"""

import json
import urllib
from urllib.request import urlopen
import urllib.parse
import urllib.error

import discord
from discord.ext import commands

from resources.config import ConfigLoader
from resources.database import DatabaseHandler


class ApiCommands():
    """Multiple commands based around the Guild Wars 2 API."""

    def __init__(self, bot):
        self.bot = bot

        self.base_url = ''
        self.header_dict = {'User-Agent': 'Mozlla/5.0'}

        self.response_url = ''
        self.header = ''
        self.data = ''

    @commands.command(pass_context=True, no_pm=False, name='api')
    @commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
    async def add_api_key(self, ctx, apikey: str, member: discord.Member=None):
        """ Add API key to bot. """
        member = ctx.message.author
        member_id = ctx.message.author.id

        if ctx.message.channel.is_private:
            if member is not None:
                row = DatabaseHandler().fetch_results(
                    "SELECT 1 FROM api WHERE discord_id = {0}".format(str(member_id)))

                if row is None:
                    permissions = ['account', 'builds', 'characters']

                    self.base_url = 'https://api.guildwars2.com/v2/tokeninfo?access_token='

                    self.response_url = self.base_url + str(apikey)
                    self.header = urllib.parse.urlencode(self.header_dict)
                    self.header = self.header.encode("utf-8")
                    response = urlopen(self.response_url)
                    response = response.read()
                    response = response.decode("utf-8")
                    self.data = json.loads(response)

                    granted_permissions = []

                    for value in self.data['permissions']:
                        granted_permissions.append(value)

                    for permission in permissions:
                        if permission not in granted_permissions:
                            return await self.bot.say(
                                "Missing required API permission(s). \
                                Require account, builds, characters."
                            )

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

    async def get_character_level(self, api_key, character_name):
        """
        This function returns character information in the format
        (exmaple) "Name: Level 80 Charr Mesmer"
        """
        self.base_url = 'https://api.guildwars2.com/v2/characters/'
        base_url2 = '/core?access_token='

        self.response_url = self.base_url + \
            str(character_name) + str(base_url2) + str(api_key)
        self.header = urllib.parse.urlencode(self.header_dict)
        self.header = self.header.encode("utf-8")
        response = urlopen(self.response_url)
        response = response.read()
        response = response.decode("utf-8")
        self.data = json.loads(response)

        character_name = character_name.replace("%20", " ")

        character_info = ''
        character_info = '{0}: Level {1} {2} {3}'.format(
            character_name, self.data['level'], self.data['race'], self.data['profession']
        )

        return character_info

    async def get_skill_ids(self, char_name, api_key, game_type):
        """Get the list of skill IDs"""
        self.base_url = 'https://api.guildwars2.com/v2/characters/'
        base_url2 = '/skills?access_token='

        self.response_url = self.base_url + \
            str(char_name) + str(base_url2) + str(api_key)
        self.header = urllib.parse.urlencode(self.header_dict)
        self.header = self.header.encode("utf-8")
        response = urlopen(self.response_url)
        response = response.read()
        response = response.decode("utf-8")
        self.data = json.loads(response)

        skill_info = {}

        for key, value in self.data['skills'][game_type].items():
            if key != 'pets':
                skill_info.update({key: value})

        return skill_info

    async def get_skill_data(self, skill_dict):
        """Gather the skill data names from the database."""
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

    async def get_trait_ids(self, char_name, api_key, game_type):
        """Get the list of trait IDs"""
        self.base_url = 'https://api.guildwars2.com/v2/characters/'
        base_url2 = '/specializations?access_token='

        self.response_url = self.base_url + \
            str(char_name) + str(base_url2) + str(api_key)
        self.header = urllib.parse.urlencode(self.header_dict)
        self.header = self.header.encode("utf-8")
        response = urlopen(self.response_url)
        response = response.read()
        response = response.decode("utf-8")
        self.data = json.loads(response)

        trait_info = []

        for item in range(len(self.data['specializations'][game_type])):
            for key, value in self.data['specializations'][game_type][item].items():
                trait_info.append({key: value})

        return trait_info

    async def get_trait_data(self, trait_dict):
        """ Except not really a dict. """
        # @TODO : could split into three functions, help make pylint stop complaining
        trait_list = []
        trait_spec_list = []

        trait_one = ''
        trait_list_one = ''

        trait_two = ''
        trait_list_two = ''

        trait_three = ''
        trait_list_three = ''

        # this is awful, but works
        for item in enumerate(trait_dict):
            for key in item[1]:
                if key == 'traits':
                    for value in item[1].values():
                        for internal_value in value:
                            trait_list.append(internal_value)
                else:
                    for value in item[1].values():
                        trait_spec_list.append(value)

        trait_one = DatabaseHandler().fetch_results(
            "SELECT spec_name FROM gw2_specs WHERE spec_id = {0}".format(int(trait_spec_list[0])))

        trait_two = DatabaseHandler().fetch_results(
            "SELECT spec_name FROM gw2_specs WHERE spec_id = {0}".format(int(trait_spec_list[1])))

        trait_three = DatabaseHandler().fetch_results(
            "SELECT spec_name FROM gw2_specs WHERE spec_id = {0}".format(int(trait_spec_list[2])))

        # we're cheating here since we know it's always 9 total traits
        for counter in range(9):
            spec_name = DatabaseHandler().fetch_results(
                "SELECT trait_name FROM gw2_traits WHERE trait_id = {0}"
                .format(int(trait_list[counter]))
            )
            if counter in range(3):
                trait_list_one = trait_list_one + ', ' + spec_name[0]
            elif counter in range(3, 6):
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
        member = ctx.message.author
        member_id = ctx.message.author.id

        server_id = str(ctx.message.server.id)

        plugin_enabled = ConfigLoader().load_server_boolean_setting(
            server_id, 'ApiCommands', 'enabled')

        # Each new part of the name needs to be upper case, so firstly we will
        # make everything lower case and then do the upper casing
        character_name = character_name.lower()
        character_name = ' '.join(word[0].upper() + word[1:] for word in character_name.split())

        # lower case the game type, just in case
        game_type = game_type.lower()

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
                        print("There was an error with the build command: {0}.".format(error_code))
                    return
            else:
                return await self.bot.say(
                    "{0.mention}, please private message me your API key."
                    .format(member)
                )


def setup(bot):
    """This makes it so we can actually use it."""
    bot.add_cog(ApiCommands(bot))
