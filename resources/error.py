import os, errno
import string
import time
import random
import datetime
import discord
from resources.config import ConfigLoader

class error_logging:
	def __init__(self):
		self.directory = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'errors'))
		self.error_message = ConfigLoader().load_config_setting('BotSettings', 'error_message')

	def create_directory(self):
		"""Create an errors directory if needed."""
		#print "DIRECTORY: %s" % (self.directory,)
		try:
			os.mkdir(self.directory)
		except OSError as exception:
			if exception.errno != errno.EEXIST:
				raise

	def generate_file(self):
		file_suffix = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
		file_suffix = file_suffix + '_{}'.format(time.strftime("%Y%m%d-%H%M%S"))
		file_name = "ERROR-LOG_{0}.log".format(file_suffix)
		file_name_and_path = "{0}/{1}".format(self.directory, file_name)
		return file_name_and_path

	async def log_error(self, error_string, error_class, user = None, bot = None):
		print('Logging error.')
		file_suffix = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
		file_suffix = file_suffix + '_{}'.format(time.strftime("%Y%m%d-%H%M%S"))
		file_name = "ERROR-LOG_{0}.log".format(file_suffix)
		with open("{0}/{1}".format(self.directory, file_name), "w+") as f:
			f.write("ERROR IN {0}, reported by {1} at {2}!\n\nException:\n {3}".format(str(error_class), str(user), str(datetime.datetime.now().time()), str(error_string)))

		if bot is not None:
			return await bot.say(self.error_message)
		else:
			print("Error log generated.")
			return

	def get_directory(self):
		return self.directory
