#pylint: disable=import-error

"""
Module for interaction with the dynamo inventory
"""

import time
import logging

from collections import defaultdict

from dyanmo.fileop.rlfsm import RLFSM
from dynamo.dataformat import Dataset
from dynamo.core.executable import inventory


LOG = logging.getLogger(__name__)


def protected_datasets(site):
    """
    :returns: the set of datasets that shouldn't be removed from a given site
    :rtype: set
    """

    acceptable_orphans = set(drobj.dataset.name for drobj in
                             inventory.sites[site].dataset_replicas())

    acceptable_orphans.update(
        dsobj.name for dsobj in inventory.datasets.itervalues() if
        dsobj.status == Dataset.STAT_IGNORED
        )

    rlfsm = RLFSM()

    # Do not delete files being transferred by Dynamo
    acceptable_orphans.update(
        rlfsm.db.query(
            """
            SELECT DISTINCT d.`name` FROM `file_subscriptions` AS u
            INNER JOIN `files` AS f ON f.`id` = u.`file_id`
            INNER JOIN `blocks` AS b ON b.`id` = f.`block_id`
            INNER JOIN `datasets` AS d ON d.`id` = b.`dataset_id`
            INNER JOIN `sites` AS s ON s.`id` = u.`site_id`
            WHERE s.`name` = %s AND u.`delete` = 0
            """,
            site
        )
    )

    rlfsm.db.close()

    return acceptable_orphans


def list_files(site):
    """
    :returns: The dynamo list of files in the inventory for a site
    :rtype: generator
    """

    now = time.time()

    for partition in inventory.sites[site].partitions.values():

        for dataset_rep, blocks in partition.replicas.iteritems():

            block_replicas = blocks or dataset_rep.block_replicas

            for block_replica in block_replicas:

                # If complete and owned,
                # then we say this replica is "old enough" to be missing
                timestamp = 0 if \
                    block_replica.is_complete() and \
                    block_replica.group.id else \
                    now

                for fileobj in block_replica.block.files:
                    yield (fileobj.lfn, fileobj.size, timestamp)


def filelist_to_blocklist(site, filelist, blocklist):
    """
    Reads in a list of files, and generates a summary of blocks

    :param str site: Used to query the inventory
    :param str filelist: Location of list of files
    :param str blocklist: Location where to write block report
    """

    # We want to track which blocks missing files are coming from
    track_missing_blocks = defaultdict(
        lambda: {'errors': 0,
                 'blocks': defaultdict(lambda: {'group': '',
                                                'errors': 0}
                                      )
                })

    blocks_query = """
                   SELECT blocks.name, IFNULL(groups.name, 'Unsubscribed') FROM blocks
                   INNER JOIN files ON files.block_id = blocks.id
                   INNER JOIN block_replicas ON block_replicas.block_id = files.block_id
                   INNER JOIN sites ON block_replicas.site_id = sites.id
                   LEFT JOIN groups ON block_replicas.group_id = groups.id
                   WHERE files.name = %s AND sites.name = %s
                   """

    with open(filelist, 'r') as input_file:
        for line in input_file:
            fileobj = inventory.find_file(line.strip())

            for replica in fileobj.block.replicas:
                if replica.site.name == site:

                    block, group = fileobj.block.name, replica.group.name

                    track_missing_blocks[dataset]['errors'] += 1
                    track_missing_blocks[dataset]['blocks'][block]['errors'] += 1
                    track_missing_blocks[dataset]['blocks'][block]['group'] = group

    # Output file with the missing datasets
    with open(blocklist, 'w') as output_file:
        for dataset, vals in \
                sorted(track_missing_blocks.iteritems(),
                       key=lambda x: x[1]['errors'],
                       reverse=True):

            for block_name, block in sorted(vals['blocks'].iteritems()):
                output_file.write('%10i    %-17s  %s#%s\n' % \
                                      (block['errors'], block['group'],
                                       dataset, block_name))
