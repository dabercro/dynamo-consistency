#pylint: disable=unused-import

"""
This module imports the commands from dynamo and CMS.
Other modules should import everything from here.
"""

import os
import sys
import json
import time

from . import filters
from .. import config

# Required abstractions from dynamo
from ..dynamo import registry
from ..dynamo import siteinfo
from ..dynamo import inventory

# Getting datasets for filtering
from ..dynamo.inventory import protected_datasets

# Check if site is ready, according to dynamo
_READY = lambda site: site in siteinfo.ready_sites()

if '--cms' in sys.argv:

    from cmstoolbox.samstatus import is_sam_good
    from ..cms.checkphedex import deletion_requests

    from ..cms.filters import DatasetFilter

    def check_site(site):
        """Checks SAM tests and dynamo"""
        return _READY(site) and is_sam_good(site)

else:

    def check_site(site):
        """Should return if the site is ready to run over or not"""
        return _READY(site)

    def deletion_requests():
        """Should return the set of deletion requests that may still be pending"""
        return set()

    class DatasetFilter(object):
        """
        .. warning::

           Needs implemented properly for vanilla dyanmo

        """
        def __init__(self, _):
            pass
        def __call__(self, _):
            """Needs a fast way to translate from name to dataset"""
            return False   # This protects nothing


if '--dry' in sys.argv:

    registry.delete = lambda *args, **kwargs: 0
    registry.transfer = lambda *args, **kwargs: 0, 0


def make_filters(site):
    """
    Creates filters proper for running environment and options

    :param str site: Site to get activity at
    :returns: Two :py:class:`filters.Filter` objects that can be used
              to check orphans and missing files respectively
    :rtype: :py:class:`filters.Filter`, :py:class:`filters.Filter`
    """

    ignore_list = config.config_dict().get('IgnoreDirectories', [])

    pattern_filter = filters.PatternFilter(ignore_list)

    # First, datasets in the deletions queue can be missing
    acceptable_missing = deletion_requests(site)
    # Orphan files cannot belong to any dataset that should be at the site
    acceptable_orphans = protected_datasets(site)
    # Orphan files may be a result of deletion requests
    acceptable_orphans.update(acceptable_missing)

    return (filters.Filter(DatasetFilter(acceptable_orphans), pattern_filter),
            filters.Filter(DatasetFilter(acceptable_missing), pattern_filter))


def extras(site, site_tree=None, debugged=False):
    """
    Runs a bunch of functions after the main consistency check,
    depending on the presence of certain arguments and configuration

    :param str site: For use to pass to extras
    :param dynamo_consistency.datatypes.DirectoryInfo site_tree: Same thing
    :param bool debugged: If not debugged, the heavier things will not be run on the site
    :returns: Dictionary with interesting results. Keys include the following:

              - ``"unmerged"`` - A tuple listing unmerged files removed and unmerged logs

    :rtype: dict
    """

    output = {}

    if debugged and '--unmerged' in sys.argv:
        from ..cms.unmerged import clean_unmerged
        output['unmerged'] = clean_unmerged(site)

    # Convert missing files to blocks
    inventory.filelist_to_blocklist(site,
                                    '%s_compare_missing.txt' % site,
                                    '%s_missing_datasets.txt' % site)

    # Make a JSON file reporting storage usage
    if site_tree and site_tree.get_num_files():
        storage = {
            'storeageservice': {
                'storageshares': [{
                    'numberoffiles': node.get_num_files(),
                    'path': [os.path.normpath('/store/%s' % subdir)],
                    'timestamp': str(int(time.time())),
                    'totalsize': 0,
                    'usedsize': node.get_directory_size()
                    } for node, subdir in [(site_tree.get_node(path), path) for path in
                                           [''] + [d.name for d in site_tree.directories]]
                                  if node.get_num_files()]
                }
            }

        with open(os.path.join(config.config_dict()['WebDir'], '%s_storage.json' % site), 'w') \
                as storage_file:
            json.dump(storage, storage_file)

    return output
