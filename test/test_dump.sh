#! /bin/bash

if which coverage
then
    coverage run --source dynamo_consistency -a $(which consistency-dump-tree) --test --site TEST_SITE
else
    consistency-dump-tree --test --site TEST_SITE
fi

diff dumptest.txt <(python -c "from dynamo_consistency.datatypes import get_info; get_info('var/cache/TEST_SITE/inventory.pkl').display()")

exit $?
