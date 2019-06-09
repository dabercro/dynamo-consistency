#! /bin/bash

for directory in "www" "var"
do

    test ! -d $directory || rm -r $directory

done

dynamo-consistency --test --lock '' || exit 1
dynamo-consistency --test --lock 'fake' && exit 2

exit 0
