"""Common utilities."""
import logging
import sys
import os

def get_logger(name):
    # type: (str) -> logging.Logger
    """Return a `Logger` instance for `name`."""
    logger = logging.getLogger(name)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(logging.DEBUG)
    return logger


def get_data_file(source_file_name):
    # type: (str) -> (str)
    """Return the data file path to store result."""
    path = list(os.path.split(source_file_name))
    path[-1] = path[-1].split('_')[0] + '.K'
    return os.path.join(*path)
