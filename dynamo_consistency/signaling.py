"""
A small module for handling signals
"""


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
""" % (config.LOCATION, config.SITE)
