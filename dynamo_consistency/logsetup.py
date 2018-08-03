"""
The module that sets up logging for us
"""

import os
import sys
import logging


LOG_FORMAT = '%(asctime)s:%(levelname)s:%(name)s: %(message)s'


if '--debug' in sys.argv:
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
elif '--info' in sys.argv:
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
else:
    logging.basicConfig(format=LOG_FORMAT)


def change_logfile(*filenames):
    """
    Changes the output file of all of the loggers.
    Creates any directories that are needed to hold the logs.

    :param filenames: The files to write new logs to
    """

    for logger in logging.Logger.manager.loggerDict.values():
        hdlr_copy = list(logger.handlers)
        for hdlr in hdlr_copy:
            logger.removeHandler(hdlr)

        for name in filenames:
            logdir = os.path.dirname(name)

            if not os.path.exists(logdir):
                os.makedirs(logdir)


            fhdl = logging.FileHandler(name, 'a')
            fhdl.setFormatter(logging.Formatter(LOG_FORMAT))

            logger.addHandler(fhdl)
