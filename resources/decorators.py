"""
@author Ryan 'iBeNifty' Malacina
@site https://snoring.ninja

decorators.py
Class for multiple different decorators
"""

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
            result = function(*args, **kwargs)
            return result
        except Exception as err:
            print("There was an error.  The reported error is: {0}"
                  .format(err)
                 )
    return wrapper
