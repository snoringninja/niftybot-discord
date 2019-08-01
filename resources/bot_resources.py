# import traceback
import configparser

from resources.config import ConfigLoader
from resources.database import DatabaseHandler
# from resources.error_logger import ErrorLogging


class BotResources:
    """
    Contains multiple different functions that are general use for different purposes that were better suited to be
    within a single class and not rewritten across classes when needed.

    @TODO: re-implement error logging
    """
    def __init__(self):
        self.prefix = ConfigLoader().load_config_setting('BotSettings', 'command_prefix')

    @staticmethod
    def check_accepted(user_id):
        """
        Check if a user has accepted the terms of service for the bot to remain Discord ToS compliant

        :param user_id: discord.Member userID
        :return: True if accepted, False if not
        """
        row = DatabaseHandler().fetch_results(
            "SELECT 1 FROM accepted_users WHERE discord_id = {0}".format(str(user_id))
        )

        if row is not None:
            return True
        return False

    @staticmethod
    def get_tos_channel_valid(server_id):
        """
        Check if the server has specified a specific channel to display the message informing a user that they
        must accept the Terms of Service before they can use certain commands.

        :param server_id: the discord server snowflake ID
        :return: True if channel specified, False if not
        """
        try:
            try:
                ConfigLoader().load_server_int_setting(
                    server_id,
                    'ConfigSettings',
                    'not_accepted_channel_id'
                )
                return True
            except ValueError:
                # ErrorLogging().log_error_without_await(
                #     traceback.format_exc(),
                #     'BotResources: get_tos_channel_id (inner)'
                # )
                return False
        except ValueError:
            # ErrorLogging().log_error_without_await(
            #     traceback.format_exc(),
            #     'BotResources: get_tos_channel_id (outer)'
            # )
            return False

    @staticmethod
    def contains_word(string, word):
        """
        Checks if a word exists within a string.  Useful for those specific circumstances where you need to know
        if a word is, in fact, within a string.

        :param string: String that is being searched for word
        :param word: The word that is being searched for
        :return: True if in string, False if not
        """
        return ' ' + word + ' ' in ' ' + string + ' '

    @staticmethod
    def load_config(default_filename):
        """
        Load the specified configuration file.

        :param default_filename: name of the config file to load
        :return: read in filename
        """
        config = configparser.ConfigParser()
        return config.read(default_filename)

    @staticmethod
    def is_valid_hour(seconds):
        """
        Check if the provided seconds is a valid hour.

        :param seconds: (int) seconds
        :return: True if valid hour, False if not
        """
        if seconds % 3600 == 0:
            return True
        return False

    @staticmethod
    def convert_seconds_to_hour(seconds):
        """
        Convert seconds to hour.

        :param seconds: (int) seconds
        :return: seconds / 3600
        """
        return seconds / 3600
