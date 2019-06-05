#! /bin/bash

for directory in "www" "var"
do

    test ! -d $directory || rm -r $directory

done

exitcode=0

dynamo-consistency --test $1

if [ $(jq '.DirectoryList | length' www/consistency_config.json) -ne 3 ]
then

    exitcode=$(($exitcode + 1))

fi

dynamo-consistency --test --config txtfiles/consistency_config.json $1

if [ $(jq '.DirectoryList | length' www/consistency_config.json) -ne 2 ]
then

    exitcode=$(($exitcode + 2))

fi

exit $exitcode
