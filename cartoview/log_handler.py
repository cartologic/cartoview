import logging
from sys import stdout

formatter = logging.Formatter(
    '[%(levelname)s %(asctime)s] {%(name)s:%(lineno)d} - %(message)s',
    '%m-%d %H:%M:%S')


def get_logger(name=__name__, with_formatter=True):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(stdout)
    if with_formatter:
        handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
