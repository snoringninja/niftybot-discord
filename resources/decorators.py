"""
@author Ryan 'iBeNifty' Malacina
@site https://snoring.ninja

decorators.py
Class for multiple different decorators
"""

import asyncio
import functools
from .error import ErrorLogging

def error_logger(function):
    """
    Decorator for logging errors
    """
    def wrapper(*args, **kwargs):
        """
        error_logger wrapper
        """
        try:
            return function(*args, **kwargs)
        except Exception as err:
            return print("There was an error.  The reported error is: {0}"
                         .format(err)
                        )
    return wrapper

@asyncio.coroutine
def error_logger_callback(function):
    """
    Coroutine decorator for logging errors
    """
    def wrapper(*args, **kwargs):
        """
        error_logger_callback wrapper
        """
        print("Oh, dear...")
        try:
            return function(*args, **kwargs)
        except Exception as err:
            return print("There was an error.  The reported error is: {0}"
                         .format(err)
                        )
    return wrapper
