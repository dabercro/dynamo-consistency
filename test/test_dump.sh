#! /bin/bash

coverage run --source dynamo_consistency -a $(which consistency-dump-tree) --test --site TEST_SITE

diff dumptest.txt <(python -c "from dynamo_consistency.datatypes import get_info; get_info('var/cache/TEST_SITE/inventory.pkl').display()")

exit $?
