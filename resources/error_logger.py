"""
error.py
@author xNifty
@site https://snoring.ninja

Handles creating the error files when called.
"""

import os
import errno
import string
import time
import random
import datetime

from .config import ConfigLoader

class ErrorLogging:
    """Create the error director, and generate error files."""
    def __init__(self):
        self.directory = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '..',
                'errors'
            )
        )
        self.error_message = ConfigLoader().load_config_setting(
            'BotSettings', 'error_message'
        )

    def create_directory(self):
        """Create an errors directory if needed."""
        #print "DIRECTORY: %s" % (self.directory,)
        try:
            os.mkdir(self.directory)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    def generate_file(self):
        """Generate the error file."""
        file_suffix = ''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits) for _ in range(6))
        file_suffix = file_suffix + '_{}'.format(time.strftime("%Y%m%d-%H%M%S"))
        file_name = "ERROR-LOG_{0}.log".format(file_suffix)
        file_name_and_path = "{0}/{1}".format(self.directory, file_name)
        return file_name_and_path

    async def log_error(self, error_string, error_class, user=None, bot=None):
        """Log the error."""
        file_suffix = ''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits) for _ in range(6))
        file_suffix = file_suffix + '_{}'.format(time.strftime("%Y%m%d-%H%M%S"))

        if error_class != 'None' or error_class is not None:
            file_name = "{0}_{1}.log".format(error_class, file_suffix)
        else:
            file_name = "ERROR-LOG_{0}.log".format(file_suffix)

        print('Logging error from {0} as {1}'.format(error_class, file_name))

        formatted_string = ''
        if isinstance(error_string, list):
            for tb_string in error_string:
                formatted_string = formatted_string + tb_string

            with open("{0}/{1}".format(self.directory, file_name), "w+") as filename:
                filename.write("ERROR IN {0}, reported by {1} at {2}!\n\nException:\n {3}"
                               .format(
                                   str(error_class),
                                   str(user),
                                   str(datetime.datetime.now().time()),
                                   formatted_string
                               )
                              )
        else:
            with open("{0}/{1}".format(self.directory, file_name), "w+") as filename:
                filename.write("ERROR IN {0}, reported by {1} at {2}!\n\nException:\n {3}"
                               .format(
                                   str(error_class),
                                   str(user),
                                   str(datetime.datetime.now().time()),
                                   str(error_string)
                               )
                              )

        if bot is not None:
            return await bot.say(self.error_message)
        return

    def log_error_without_await(self, error_string, error_class):
        """Log an error without the need to await."""
        print('Logging error.')
        file_suffix = ''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits) for _ in range(6))
        file_suffix = file_suffix + '_{}'.format(time.strftime("%Y%m%d-%H%M%S"))
        file_name = "ERROR-LOG_{0}.log".format(file_suffix)
        with open("{0}/{1}".format(self.directory, file_name), "w+") as filename:
            filename.write("ERROR IN {0}, reported at {1}!\n\nException:\n {2}"
                           .format(
                               str(error_class),
                               str(datetime.datetime.now().time()),
                               str(error_string)
                           )
                          )

        print("Error log generated.")
        return

    def get_directory(self):
        """Get the error directory."""
        return self.directory
    