"""
This module defines any filters that are used specifically for CMS.
"""

import logging


LOG = logging.getLogger(__file__)


class DatasetFilter(object):
    """
    Filter to check if files are in the CMS-style datasets
    """

    def __init__(self, datasets):
        self.datasets = datasets

def dataset_filter(file_name, datasets):
    """
    Returns whether the file is in a dataset that is "acceptable".
    In other words, the datasets parameter should include datasets
    to be taken out of the results returned by
    :py:module:`dynamo_consistency.datatypes.compare`.
    If the file name is not structured in a way to get the dataset out,
    then this function chooses to filter it out.

    :param str file_name: Full LFN of file
    :param set datasets: Set (or other collection) of datasets
                         using CMS notation
    :returns: If file belongs to dataset
    :rtype: bool
    """

    LOG.debug('Checking file_name: %s', file_name)

    split_name = file_name.split('/')

        try:
            return '/%s/%s-%s/%s' % (split_name[4], split_name[3],
                                     split_name[6], split_name[5]) in acceptable
        except IndexError:
            LOG.warning('Strange file name: %s', file_name)
            return True
