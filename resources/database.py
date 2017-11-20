"""Niftybot
# @author - Ryan Malacina (xNifty)
# database.py
# Functions: Handle the SQLite stuff
"""

import os

import sqlite3
from resources.config import ConfigLoader

class DatabaseHandler(object):
    """DatabaseHandler

    Class to handle all functions related to
    database manipulation.
    """
    # @TODO : need a database generation script
    # @TODO : close connection
    # @TODO : NEED TO USE PARAMATIZED QUERIES EVERY TIME

    def __init__(self):
        self.path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '../'
            )
        )

        self.sqlite_database = os.path.join(
            self.path,
            ConfigLoader().load_config_setting(
                'BotSettings',
                'sqlite'
            )
        )

    def connected_to_sqlite(self):
        """Check if connection to the
        SQLite database can be made.
        """
        connected = False
        try:
            connection = sqlite3.connect(self.sqlite_database)
            connected = True
        except sqlite3.Error as db_error:
            print("connected_to_sqlite error: {0}".format(db_error))
        finally:
            if connected:
                connection.close()
        return

    def fetch_results(self, query):
        """Fetch a single result from the database.
        """
        try:
            database = sqlite3.connect(self.sqlite_database)
            cursor = database.cursor()
            executed = cursor.execute(query)
            result = executed.fetchone()
            database.close()
        except sqlite3.Error as db_error:
            return print("fetch_results error: {0}".format(db_error))
        return result

    def fetch_all_results(self, query):
        """Fetch all matching results.

        :query: query to be run, without passed arguments
        """
        try:
            database = sqlite3.connect(
                self.sqlite_database,
                detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES
            )
            cursor = database.cursor()
            executed = cursor.execute(query)
            result = executed.fetchall()
            database.close()
        except sqlite3.Error as db_error:
            return print("fetch_all_results error: {0}".format(db_error))
        return result

    def update_database(self, query):
        """Update an entry in the database, without
        passing any arguments.

        :query: query to be run, without passed arguments
        """
        try:
            database = sqlite3.connect(
                self.sqlite_database,
                detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES
            )
            cursor = database.cursor()
            cursor.execute(query)
            database.commit()
            database.close()
        except sqlite3.Error as db_error:
            return print("update_database error: {0}".format(db_error))
        return

    def update_database_with_args(self, query, args):
        """Update an entry in the database, accepts arguments

        :query: query to be run
        :args: arguments passed alongside the query
        """
        try:
            database = sqlite3.connect(
                self.sqlite_database,
                detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES
            )
            cursor = database.cursor()
            cursor.execute(query, args)
            database.commit()
            database.close()
        except sqlite3.Error as db_error:
            return print("update_database_with_args error: {0}".format(db_error))
        return

    def insert_into_database(self, query, params):
        """Insert a result into the database.

        :query: query to be run
        :params: parameters passed alongside the query
        """
        try:
            database = sqlite3.connect(
                self.sqlite_database,
                detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES
            )
            cursor = database.cursor()
            result = cursor.execute(query, params)
            database.commit()
            new_row = result.fetchone()
            database.close()
        except sqlite3.Error as db_error:
            return print("insert_into_database error: {0}".format(db_error))
        return new_row
