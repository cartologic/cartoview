from sys import stdout
import logging
formatter = logging.Formatter(
    '[%(asctime)s] p%(process)s  { %(name)s %(pathname)s:%(lineno)d} \
                            %(levelname)s - %(message)s', '%m-%d %H:%M:%S')


def get_logger(name=__name__):
    logger = logging.getLogger(name)
    handler = logging.StreamHandler(stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
