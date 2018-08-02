"""
The module that sets up logging for us
"""


import sys
import logging


_LOG_FORMAT = '%(asctime)s:%(levelname)s:%(name)s: %(message)s'


if 'debug' in sys.argv:
    logging.basicConfig(level=logging.DEBUG, format=_LOG_FORMAT)
elif 'watch' in sys.argv:
    logging.basicConfig(level=logging.INFO, format=_LOG_FORMAT)
else:
    logging.basicConfig(format=_LOG_FORMAT)
