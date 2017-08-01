import os
import sys

class resourcepath():
	def __init__(self):
		self.random_unused_variable = '' # this literally is not used for anything but placing something in __init__

	def resource_path(self, relative):
		if hasattr(sys, "_MEIPASS"):
			return os.path.join(sys._MEIPASS, relative)
		return os.path.join(relative)