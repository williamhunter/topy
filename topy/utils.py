"""Common utilities."""
import logging
import sys

def get_logger(name):
    # type: (str) -> logging.Logger
    """Return a `Logger` instance for `name`."""
    logger = logging.getLogger(name)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(logging.DEBUG)
    return logger