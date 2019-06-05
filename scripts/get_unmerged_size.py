#! /usr/bin/env python

import os
import sys

from dynamo_consistency.datatypes import get_info

site = sys.argv[1]
# Should actually get these from config JSON file
cache_dir = '/slocal/dynamo/consistency/cache'
web_dir = '/home/dynamo/consistency/web'

# Load in files first
with open(os.path.join(web_dir, '%s_unmerged.txt' % site), 'r') as deleted:
    files = [line.strip() for line in deleted if line.strip()]

if len(files):
    # Only load this in if we have files to check
    unmerged = get_info(os.path.join(cache_dir, '%s/unmerged.pkl%s' % (site, os.environ.get('suff', ''))))
    # Print the sum of the file sizes
    to_delete = sum([unmerged.get_file(f)['size'] for f in files if not f.endswith('.')])
    print 'To delete: %s (%s TBs)' % (to_delete, to_delete/pow(1024., 4))
    print 'Total: %s' % unmerged.get_directory_size()

else:
    print 'No files to delete!'
    exit(0)

# Then let's do no timing info:

from cmstoolbox.unmergedcleaner import listdeletable

listdeletable.set_config('/home/dabercro/dev_python/consistency_config.json', 'ListDeletable')
listdeletable.PROTECTED_LIST = listdeletable.get_protected()
listdeletable.PROTECTED_LIST.sort()

deletion_file = '/home/dabercro/dev_python/dynamo-consistency/notime.txt'
listdeletable.config.DELETION_FILE = deletion_file

listdeletable.get_unmerged_files = lambda: unmerged.get_files(0)
listdeletable.main()

if unmerged.get_node('unmerged/logs', make_new=False):
    with open(deletion_file, 'a') as d_file:
        d_file.write('\n' + '\n'.join(
                unmerged.get_node('unmerged/logs').get_files(
                    min_age=0,
                    path='/store/unmerged')))


with open(deletion_file, 'r') as deleted:
    files = [line.strip() for line in deleted if line.strip()]

print 'No time limit'

if len(files):
    # Print the sum of the file sizes
    print 'To delete: %s' % sum([unmerged.get_file(f)['size'] for f in files if not f.endswith('.')])
    print 'Total: %s' % unmerged.get_directory_size()

else:
    print 'No files to delete!'
    exit(0)
