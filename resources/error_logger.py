import os
import errno
import string
import time
import random
import datetime

from .config import ConfigLoader


class ErrorLogging:
    """
    Handles all error logging for the bot.  We use this instead of the error handling that comes with discord.py,
    as it was bulky and tended to spam the console instead of generating easy to read later error logs.

    This cleans that up and lets us generate files that can be looked at later as needed.  This is not in use by
    default, and any new cogs, plugins, etc. need to explicitly set it up to catch errors and generate logs.
    """
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
        """
        So right now, this is not done in a clean fashion.  Instead of how it currently is (which is, we just try
        to create the directory and see if we get an error that it already exists), we really should just check if it
        exists and create it if it does not.  Anyways...if the directory exists, we continue on by checking which error
        is returned.  If the error is not that the directory exists, we raise an error otherwise we just do nothing.
        
        :return: Nothing
        """""
        # print "DIRECTORY: %s" % (self.directory,)
        try:
            os.mkdir(self.directory)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    def generate_file(self):
        """
        Generate the error log.  May be deprecated and replaced with log_error, but may have been kept as it allows
        error log generating without the requirement of passing which class the error was generated from.  Would not
        recommend using this unless you absolutely have a reason to. (@TODO: remove completely?)

        :return: Nothing
        """
        file_suffix = ''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits) for _ in range(6))
        file_suffix = file_suffix + '_{}'.format(time.strftime("%Y%m%d-%H%M%S"))
        file_name = "ERROR-LOG_{0}.log".format(file_suffix)
        file_name_and_path = "{0}/{1}".format(self.directory, file_name)
        return file_name_and_path

    async def log_error(self, error_string, error_class, user=None, bot=None):
        """
        Log an error and generate the file, using the error_class if provided to give the file a name that makes it
        clear which error it is.  Also timestamp all errors to prevent issues of duplicate file names.

        If no error_class is provided, the file will still generate but is simply called ERROR-LOG_datetime instead.

        :param error_string: (str) String that contains the error message / traceback information
        :param error_class: (str) Class that the error occurred in
        :param user: User that generated the error (optional parameter)
        :param bot: Bot object, required to print out a message to the user/channel that something went wrong
        :return: Nothing
        """
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
        """
        Log an error and generate the file, without the need to await anything.  Not entirely sure if working at this
        point, or what the reasoning behind it was, but not yet removed until that information is available.

        :param error_string: (str) String that contains the error message / traceback information
        :param error_class: Nothing
        """
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
        """
        Simple returns the error directory.

        :return: self.directory
        """
        return self.directory
