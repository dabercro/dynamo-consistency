"""
The module that sets up logging for us
"""

import os
import logging

from . import opts

LOG_FORMAT = '%(asctime)s:%(levelname)s:%(name)s: %(message)s'


if opts.DEBUG:
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
elif opts.INFO:
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
else:
    logging.basicConfig(format=LOG_FORMAT)


def change_logfile(*filenames):
    """
    Changes the output file of all of the loggers.
    Creates any directories that are needed to hold the logs.

    :param filenames: The files to write new logs to
    """

    new_hldrs = []

    for name in filenames:
        logdir = os.path.dirname(name)

        if not os.path.exists(logdir):
            os.makedirs(logdir)

        fhdl = logging.FileHandler(name, 'a')
        fhdl.setFormatter(logging.Formatter(LOG_FORMAT))

        new_hldrs.append(fhdl)

    for logger in logging.Logger.manager.loggerDict.values():
        if not isinstance(logger, logging.Logger):
            continue

        hdlr_copy = list(logger.handlers)
        for hdlr in hdlr_copy:
            logger.removeHandler(hdlr)

        for fhdl in new_hldrs:
            logger.addHandler(fhdl)
