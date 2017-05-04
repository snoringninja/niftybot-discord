import cgitb, os, errno

direc = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'errors'))

cgitb.enable(logdir=os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'errors')), display=False, format='text')

class error_logging:
	def __init__(self):
		self.directory = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'errors'))

	def create_directory(self):
		"""Create an errors directory if needed."""
		#print "DIRECTORY: %s" % (self.directory,)
		try:
			os.mkdir(self.directory)
		except OSError as exception:
			if exception.errno != errno.EEXIST:
				raise

	def get_directory(self):
		return self.directory
