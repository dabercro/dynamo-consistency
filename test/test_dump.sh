#! /bin/bash

test ! -d var || rm -rf var

if which coverage
then
    coverage run --source dynamo_consistency -a $(which consistency-dump-tree) --test --site TEST_SITE
else
    consistency-dump-tree --test --site TEST_SITE
fi

diff txtfiles/dumptest.txt <(python -c "from dynamo_consistency.datatypes import get_info; get_info('var/cache/TEST_SITE/inventory.pkl').display()") || exit 1

consistency-dump-tree --test --site TEST_SITE funny_name
diff txtfiles/dumptest.txt <(python -c "from dynamo_consistency.datatypes import get_info; get_info('var/cache/TEST_SITE/funny_name.pkl').display()") || exit 2

# Check the remote switch
consistency-dump-tree --test --site TEST_SITE --remote
diff txtfiles/remotelist.txt <(python -c "from dynamo_consistency.datatypes import get_info; get_info('var/cache/TEST_SITE/remote.pkl').display()") || exit 3
