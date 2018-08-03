#pylint: disable=unused-import

"""
This module imports the commands from dynamo and CMS.
Other modules should import everything from here.
"""

import os
import sys
import json
import time

from .. import opts
from .. import config

# Required abstractions from dynamo
from ..dynamo import registry
from ..dynamo import siteinfo
from ..dynamo import inventory

# Getting datasets for filtering
from ..dynamo.inventory import protected_datasets

# Check if site is ready, according to dynamo
_READY = lambda site: site in siteinfo.ready_sites()

if opts.CMS:

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

        @staticmethod
        def protected(_):
            """Needs a fast way to translate from name to dataset"""
            return False    # This protects nothing


if not opts.REPORT:

    registry.delete = lambda *args, **kwargs: 0
    registry.transfer = lambda *args, **kwargs: 0, 0
