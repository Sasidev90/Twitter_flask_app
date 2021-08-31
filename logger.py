import logging
from logging.handlers import TimedRotatingFileHandler
import os

ROOT = os.getcwd()
path_trace = os.getcwd() + '\logs\\traces.log'
path_exe = os.getcwd() + '\logs\\exceptions.log'

if not os.path.exists(path_trace):
    with open(path_trace, 'w') as fp:
        pass

if not os.path.exists(path_exe):
    with open(path_exe, 'w') as fp:
        pass

formatter = logging.Formatter('%(levelname)s | %(asctime)s | module: %(module)s | lineno: %(lineno)d | %(message)s')


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    fh = TimedRotatingFileHandler(log_file, when='midnight')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


trace = setup_logger('first_logger', 'logs/traces.log')
exc = setup_logger('second_logger', 'logs/exceptions.log')
