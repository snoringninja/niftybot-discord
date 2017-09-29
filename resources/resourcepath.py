"""
resourcepath.py
@author Ryan 'iBeNifty' Malacina
@site https://snoring.ninja
"""

import os

class resourcepath():
    """Returns the provide resource path."""
    def resource_path(self, relative):
        """Return the path."""
        return os.path.join(relative)