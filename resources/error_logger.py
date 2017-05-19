# exception_logger.py
 
import logging
import os, errno
import time
import random
import datetime
import string

def create_logger():
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger("example_logger")
    logger.setLevel(logging.INFO)

    file_suffix = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
    file_suffix = file_suffix + '_{}'.format(time.strftime("Y%m%d-%H%M%S"))
    file_name = "ERROR-LOG_{0}.log".format(file_suffix)
 
    # create the logging file handler
    fh = logging.FileHandler(r"{0}".format(file_name))
 
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
 
    # add handler to logger object
    logger.addHandler(fh)
    return logger
 
logger = create_logger()
