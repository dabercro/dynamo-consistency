"""
A module to handle file dumps from sites
"""


import os
import time
import datetime

from .. import config


class LineReader(object):
    """
    A class that translates lines from a file dump.
    It tracks the time that it was initialized.
    """

    def __init__(self):
        self.now = int(time.time())

    def __call__(self, line):
        """
        :param str line: Single line from a file dump
        :returns: The useful information from a line
        :rtype: tuple
        """

        contents = line.split()
        return contents[0], int(contents[2]), self.now


def read_ral_dump(endpoint, datestring=None):
    """
    Copies file from remote site and lists
    :param str endpoint: The SE to copy the file dump from
    :param str datestring: An optional datestring to force source file name
    :returns: A tuple of the filename and translator
    :rtype: tuple
    """

    inputfile = os.path.join(config.vardir('scratch'), 'dump_%s' % config.SITE)

    os.system(
        'gfal-copy {endpoint}/store/accounting/dump_{date} {target}.raw'.format(
            endpoint=endpoint,
            date=datestring or datetime.datetime.utcnow().strftime('%y%m%d'),
            target=inputfile
            )
        )
    os.system('sort -o {target} {target}.raw'.format(target=inputfile))

    return inputfile, LineReader()
