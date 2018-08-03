"""
Holds the main function for running the consistency check
"""

import logging
import os
import shutil
import time
import datetime


from . import config
from . import inventorylister
from . import remotelister
from . import datatypes
from . import summary
from .backend import make_filters
from .backend import registry
from .backend import extras
from .backend.emptyremover import EmptyRemover


LOG = logging.getLogger(__name__)


# Need to make this smaller
def main(site):    #pylint: disable=too-many-locals
    """
    Gets the listing from the dynamo database, and remote XRootD listings of a given site.
    The differences are compared to deletion queues and other things.

    The differences that should be acted on are copied to the summary webpage
    and entered into the dynamoregister database.

    :param str site: The site to run the check over
    """

    start = time.time()

    inv_tree = inventorylister.listing(site)

    # Reset the DirectoryList for the XRootDLister to run on
    config.DIRECTORYLIST = [directory.name for directory in inv_tree.directories]
    remover = EmptyRemover(site)
    site_tree = remotelister.listing(site, remover)

    check_orphans, check_missing = make_filters(site)

    # Do the comparison
    missing, m_size, orphan, o_size = datatypes.compare(
        inv_tree, site_tree, '%s_compare' % site,
        orphan_check=check_orphans, missing_check=check_missing)

    LOG.info('Missing size: %i, Orphan size: %i', m_size, o_size)

    # Determine if files should be entered into the registry

    config_dict = config.config_dict()

    many_missing = len(missing) > int(config_dict['MaxMissing'])
    many_orphans = len(orphan) > int(config_dict['MaxOrphan'])

    # Track files with no sources
    no_source_files = []
    unrecoverable = []

    # Filter out missing files that were not missing previously
    config_dict = config.config_dict()

    prev_missing = os.path.join(config_dict['WebDir'], '%s_compare_missing.txt' % site)
    prev_set = set()

    if os.path.exists(prev_missing):
        with open(prev_missing, 'r') as prev_file:
            for line in prev_file:
                prev_set.add(line.strip())

        if int(config_dict.get('SaveCache')):
            prev_new_name = '%s.%s' % (prev_missing,
                                       datetime.datetime.fromtimestamp(
                                           os.stat(prev_missing).st_mtime).strftime('%y%m%d')
                                      )
        else:
            prev_new_name = prev_missing

        shutil.move(prev_missing,
                    os.path.join(config_dict['CacheLocation'],
                                 prev_new_name)
                   )

    if summary.is_debugged(site) and not many_missing and not many_orphans:
        # Only get the empty nodes that are not in the inventory tree
        registry.delete(site,
                        orphan + [empty_node for empty_node in site_tree.empty_nodes_list() \
                                      if not inv_tree.get_node('/'.join(empty_node.split('/')[2:]),
                                                               make_new=False)]
                       )

        no_source_files, unrecoverable = registry.transfer(
            site, [f for f in missing if f in prev_set or not prev_set])

    else:

        if many_missing:
            LOG.error('Too many missing files: %i, you should investigate.', len(missing))

        if many_orphans:
            LOG.error('Too many orphan files: %i out of %i, you should investigate.',
                      len(orphan), site_tree.get_num_files())


    with open('%s_missing_nosite.txt' % site, 'w') as nosite:
        for line in no_source_files:
            nosite.write(line + '\n')

    with open('%s_unrecoverable.txt' % site, 'w') as output_file:
        output_file.write('\n'.join(unrecoverable))

    extras_results = extras(site, site_tree, summary.is_debugged(site))

    unmerged, unmergedlogs = extras_results.get('unmerged', (0, 0))

    # If one of these is set by hand, then probably reloading cache,
    # so don't update the summary table
    if (os.environ.get('ListAge') is None) and (os.environ.get('InventoryAge') is None):

        unlisted = site_tree.get_unlisted()

        summary.update_summary(
            site=site,
            duration=time.time() - start,
            numfiles=site_tree.get_num_files(),
            numnodes=remover.get_removed_count() + site_tree.count_nodes(),
            numempty=remover.get_removed_count() + len(site_tree.empty_nodes_list()),
            nummissing=len(missing),
            missingsize=m_size,
            numorphan=len(orphan),
            orphansize=o_size,
            numnosource=len(no_source_files),
            numunrecoverable=len(unrecoverable),
            numunlisted=len(unlisted),
            numbadunlisted=len([d for d in unlisted
                                if True not in [i in d for i in config_dict['IgnoreDirectories']]]),
            numunmerged=unmerged,
            numlogs=unmergedlogs)

        summary.move_local_files(site)
