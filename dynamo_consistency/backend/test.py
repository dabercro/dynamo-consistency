# pylint: disable=missing-docstring, unused-argument, invalid-name

"""
This module defines dummy variables as needed by
dynamo_consistency.backend for running tests with
"""


import os

from .. import config

# These are all the methods needed from inventory
class _Inventory(object):
    @staticmethod
    def protected_datasets(site):
        return set()
    @staticmethod
    def list_files(site):
        return list()


class _Registry(object):
    def __init__(self):
        self.deleted = []
        self.transfered = []

    def delete(self, site, files):
        self.deleted = sorted(files) # This overwrites previous deletion call
        return len(files)

    def transfer(self, site, files):
        # This overwrites previous transfer call
        self.transfered = [(site, fil) for fil in files]
        return [], []


class _SiteInfo(object):
    @staticmethod
    def site_list():
        return ['TEST_SITE', 'BAD_SITE']
    @staticmethod
    def ready_sites():
        return set(['TEST_SITE'])


TMP_DIR = 'TempConsistency'


def _ls(path, location=TMP_DIR):

    full_path = os.path.join(location, path[len(config.config_dict()['RootPath']) + 1:])
    results = [os.path.join(full_path, res) for res in os.listdir(full_path)]

    dirs = [(os.path.basename(name), os.stat(name).st_mtime)
            for name in results if os.path.isdir(name)]
    files = [(os.path.basename(name), os.stat(name).st_size, os.stat(name).st_mtime)
             for name in results if os.path.isfile(name)]

    return True, dirs, files


# The following are all the things imported by dynamo_consistency.backend

inventory = _Inventory()
registry = _Registry()
siteinfo = _SiteInfo()

def filelist_to_blocklist(site, infile, outfile):
    pass

def get_listers(site):
    return _ls, None

def check_site(site):
    return site in siteinfo.ready_sites()

def deletion_requests(site):
    return set()

class DatasetFilter(object):
    def __init__(self, _):
        pass
    @staticmethod
    def protected(_):
        return False
