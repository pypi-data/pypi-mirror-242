"""
Logger utilities for the spine package.
"""
import logging
import functools
from functools import wraps
from time import time

class CustomFormatter(logging.Formatter):
    """
    Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629

    This CustomFormatter is set with is_header=True, otherwise general information
    should be logged in standard white text.
    """

    red = "\x1b[31;20m"
    magenta = '\x1b[0;35m'
    reset = '\x1b[0m'

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.INFO: self.magenta + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def log_to_console(logger_name, is_header=False, if_n_handlers = 0):
    '''
    Set logger configurations.

    args:
        logger_name (str): name of the logger
        is_header (bool): whether to log info in magenta
        if_n_handlers (int): number of handlers to add to the logger
    '''
    logger = logging.getLogger(logger_name)

    if len(logger.handlers) == if_n_handlers:
        logger.setLevel(logging.INFO)

        # Make stream handler to log to console
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Make file handler to log to file
        fh = logging.FileHandler("logs.log")
        fh.setLevel(logging.INFO)

        # Set format of log messages
        formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        fh.setFormatter(logging.Formatter(formatter))

        if is_header:
            ch.setFormatter(CustomFormatter(formatter))
        else:
            ch.setFormatter(logging.Formatter(formatter))

        # Add handlers to logger
        logger.addHandler(ch)
        logger.addHandler(fh)


def exception(logger):
    '''
    returns decorator logging exceptions
    of the wrapped function with the given logger.

    args:
      logger (logging.Logger): a logger
    returns:
        decorator (function): a decorator function
    '''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as err:
                logger.exception(f'Exception occured in {func.__name__}')
                raise
        return wrapper
    return decorator

def timing(logger):
    '''
    returns decorator that logs the total execution time
    of the wrapped function with the given logger.

    args:
        logger (logging.Logger): a logger
    returns:
        decorator (function): a dsecorator function
    '''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info('{}: Start'.format(func.__name__))
            start = time()
            result = func(*args, **kwargs)
            duration = time()-start
            if duration > 3600:
                duration = duration/3600
                units = 'hrs'
            elif duration > 60:
                duration = duration/60
                units = 'min'
            else:
                units = 'sec'
            logger.info('{}: End ({:.4f} {})'.format(func.__name__, duration, units))
            return result
        return wrapper
    return decorator