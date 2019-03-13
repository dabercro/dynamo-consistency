#! /bin/bash

# Only run where dynamo is installed
which dynamo || exit 0

cd /work || exit 1

conf=$PWD/test/dynamo/consistency_config.json
check=$PWD/test/dynamo/checkhistory.py

# Assume we're inside a Docker container
mkdir -p var/cache/T3_US_MIT
mv remote.pkl var/cache/T3_US_MIT

dynamo "`which dynamo-consistency` --site T3_US_MIT --info --v1 --config $conf" || exit 4

$check || exit 2

# Check inventory object use
dynamo "`which dynamo-consistency` --site T3_US_MIT --info --config $conf" || exit 5

$check || exit 3
