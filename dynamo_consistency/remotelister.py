"""
Tool to get the files located at a site.

:author: Daniel Abercrombie <dabercro@mit.edu> \n
         Max Goncharov <maxi@mit.edu>
"""

import logging

from . import config
from . import datatypes

from .backend import listers
from .backend import redirectors
from .backend.cache import cache_tree


LOG = logging.getLogger(__name__)


@cache_tree('ListAge', 'remote')
def listing(site, callback=None):
    """
    Get the information for a site, from XRootD or a cache.

    :param str site: The site name
    :param function callback: The callback function to pass to :py:func:`datatypes.create_dirinfo`
    :returns: The site directory listing information
    :rtype: dynamo_consistency.datatypes.DirectoryInfo
    """

    config_dict = config.config_dict()
    access = config_dict.get('AccessMethod', {})
    if access.get(site) == 'SRM':
        num_threads = int(config_dict.get('GFALThreads'))
        LOG.info('threads = %i', num_threads)
        directories = [
            datatypes.create_dirinfo('/store', directory, listers.GFalLister,
                                     [(site, x) for x in xrange(num_threads)], callback) \
                for directory in config.config_dict().get('DirectoryList', [])
        ]
        # Return the DirectoryInfo
        return datatypes.DirectoryInfo(name='/store', directories=directories)

    # Get the redirector for a site
    # The redirector can be used for a double check (not implemented yet...)
    # The redir_list is used for the original listing
    num_threads = int(config_dict.get('NumThreads'))

    balancer, door_list = redirectors.get_redirector(site)
    LOG.debug('Full redirector list: %s', door_list)

    if site in config_dict.get('UseLoadBalancer', []) or \
            (balancer and not door_list):
        num_threads = 1
        door_list = [balancer]

    if not door_list:
        LOG.error('No doors found. Returning emtpy tree')
        return datatypes.DirectoryInfo(name='/store')

    while num_threads > len(door_list):
        if len(door_list) % 2:
            door_list.extend(door_list)
        else:
            # If even number of redirectors and not using both, stagger them
            door_list.extend(door_list[1:])
            door_list.append(door_list[0])

    # Strip off the extra threads
    door_list = door_list[:num_threads]

    # Create DirectoryInfo for each directory to search (set in configuration file)
    # The search is done with XRootDLister objects that have two doors and the thread
    # number as initialization arguments.

    directories = [
        datatypes.create_dirinfo(
            '/store/', directory,
            listers.XRootDSubShell if access.get(site) == 'directx' else listers.XRootDLister,
            [(site, door, thread_num) for thread_num, door in enumerate(door_list)],
            callback) for directory in config_dict.get('DirectoryList', [])
        ]

    # Return the DirectoryInfo
    return datatypes.DirectoryInfo(name='/store', directories=directories)
