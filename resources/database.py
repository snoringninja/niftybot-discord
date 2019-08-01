import os
import sqlite3

from resources.config import ConfigLoader


class DatabaseHandler(object):
    """
    class DatabaseHandler

    Handles all database manipulation functions (e.g. select, insert, update, delete), as well as connecting to the
    database itself.
    """
    # @TODO : need a database generation script
    # @TODO : NEED TO USE PARAMETRIZED QUERIES EVERY TIME

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
        """
        Checks if a connection can be made to the SQLite database that is specified in the bot configuration.
        :return: Nothing
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
        """
        Fetches a single result from the database based on the query provided.

        :param query: (str) query to be run, without passed arguments
        :return: result
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
        """
        Fetches all matching results for the query that is run.

        :param query: query to be run, without passed arguments
        :return: result
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
        """
        Update an entry in the database, without passing any arguments.

        :param query: query to be run, without passed arguments
        :return: Nothing
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

    def update_database_with_args(self, query, params):
        """
        Update an entry in the database, using a query that optionally accepts parameters

        :param query: query to be run
        :param params: arguments passed alongside the query
        :return: Nothing
        """
        try:
            database = sqlite3.connect(
                self.sqlite_database,
                detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
            )
            cursor = database.cursor()
            cursor.execute(query, params)
            database.commit()
            database.close()
        except sqlite3.Error as db_error:
            return print("update_database_with_args error: {0}".format(db_error))
        return

    def insert_into_database(self, query, params):
        """
        Insert a result into the database, using a query that optionally accepts parameters

        :param query: query to be run
        :param params: parameters passed alongside the query
        :return: Nothing
        """
        try:
            database = sqlite3.connect(
                self.sqlite_database,
                detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
            )
            cursor = database.cursor()
            result = cursor.execute(query, params)
            database.commit()
            new_row = result.fetchone()
            database.close()
        except sqlite3.Error as db_error:
            return print("insert_into_database error: {0}".format(db_error))
        return new_row
