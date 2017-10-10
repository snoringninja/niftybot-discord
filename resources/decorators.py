"""
@author Ryan 'iBeNifty' Malacina
@site https://snoring.ninja

decorators.py
Class for multiple different decorators
"""

import asyncio
from .error import ErrorLogging

def error_logger(function):
    """
    Decorator for logging errors
    """
    def wrapper():
        """
        error_logger wrapper
        """
        try:
            function()
        except Exception as err:
            print("There was an error.  The reported error is: {1}"
                  .format(err)
                 )
    return wrapper
