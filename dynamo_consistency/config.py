"""
Small module to get information from the config.

:author: Daniel Abercrombie <dabercro@mit.edu>
"""


import os
import logging
import json


LOG = logging.getLogger(__name__)
CONFIG_FILE = 'consistency_config.json'
"""
The string giving the location of the configuration JSON file.
Generally, you want to set this value of the module before calling
:py:func:`config_dict` to get your configuration.
"""
LOADER = json
"""
A module that uses the load function on a file descriptor to return a dictionary.
(Examples are the ``json`` and ``yaml`` modules.)
If your ``CONFIG_FILE`` is not a JSON file, you'll want to change this
also before calling :py:func:`config_dict`.
"""

DIRECTORYLIST = None
"""
If this is set to a list of directories, it overrides the
``DirectoryList`` set in the configuration file.
This prevents the tool from attempting to list directories that are not there.
"""

CONFIG = None


def config_dict():
    """
    This only loads the configuration file the first time it is called

    :returns: the configuration file in a dictionary
    :rtype: str
    :raises IOError: when it cannot find the configuration file
    """

    #pylint: disable=global-statement

    global CONFIG
    global DIRECTORYLIST

    if CONFIG is None:

        location = CONFIG_FILE

        # If not there, fall back to the test directory
        # This is mostly so that Travis-CI finds a configuration on it's own
        if not os.path.exists(location):
            LOG.warning('Could not find file at %s. '
                        'Set the value of config.CONFIG_FILE to avoid receiving this message',
                        location)
            location = os.path.join(os.path.dirname(__file__),
                                    CONFIG_FILE)
            LOG.warning('Falling back to test configuration: %s', location)

        # If file exists, load it
        if os.path.exists(location):
            with open(location, 'r') as config:
                LOG.debug('Opening config: %s', location)
                CONFIG = LOADER.load(config)
        else:
            raise IOError('Could not load config at ' + location)

        # Overwrite any values with environment variables
        for key in CONFIG.keys():
            CONFIG[key] = os.environ.get(key, CONFIG[key])

    # If DIRECTORYLIST set, overwrite previous entry
    if DIRECTORYLIST:
        CONFIG['DirectoryList'] = DIRECTORYLIST
        # Only do this writing once
        DIRECTORYLIST = None

    return CONFIG
