#! /bin/bash

# Make sure we're in the test directory
cd $(dirname $0)

for directory in "www" "var"
do

    test ! -d $directory || rm -r $directory

done

exitcode=0

dynamo-consistency --test --info

test -f www/consistency_config.json || exitcode=$(($exitcode + 1))

exit $exitcode
