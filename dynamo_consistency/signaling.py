"""
A small module for handling signals
"""

import os

from . import config


def no_interrupt(*_):
    """
    Gives a message to the person who attempted the interrupt
    to use ``set-status`` instead.
    """

    print """
  Please do not cancel threaded applications this way.
  Run the following instead:

    set-status --config %s %s halt
""" % (os.path.abspath(config.LOCATION), config.SITE)
