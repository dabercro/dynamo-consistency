#! /usr/bin/env python

import os
import sys

from dynamo_consistency.datatypes import get_info

site = sys.argv[1]
# Should actually get these from config JSON file
cache_dir = '/local/dynamo/consistency/cache'
web_dir = '/home/dynamo/consistency/web'

# Load in files first
with open(os.path.join(web_dir, '%s_unmerged.txt' % site), 'r') as deleted:
    files = [line.strip() for line in deleted]

if len(files):
    # Only load this in if we have files to check
    unmerged = get_info(os.path.join(cache_dir, '%s_unmerged.pkl' % site))
    # Print the sum of the file sizes
    print sum([unmerged.get_file(f)['size'] for f in files])

else:
    print 'No files to delete!'
