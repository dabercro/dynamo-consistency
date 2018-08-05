#! /bin/bash

ec=0

_check () {

    site=$1
    isrunning=$2
    isgood=$3

    dbrunning=$(echo "SELECT isrunning FROM sites WHERE site='$site';" | sqlite3 www/stats.db)
    dbgood=$(echo "SELECT isgood FROM sites WHERE site='$site';" | sqlite3 www/stats.db)

    if [ "$isrunning" != "$dbrunning" ]
    then
        echo "Bad running for $site: expected $isrunning got $dbrunning"
        ec=$(( $ec + 1 ))
    fi

    if [ "$isgood" != "$dbgood" ]
    then
        echo "Bad good for $site: expected $isgood got $dbgood"
        ec=$(( $ec + 1 ))
    fi

}

if [ -d www ]
then

    rm -r www

fi

consistency-web-install --test

# Check starting status
_check BAD_SITE "-1" "0"   # Only because it's first alphabetically
_check TEST_SITE "0" "0"

set-status --test TEST_SITE act
_check TEST_SITE "0" "1"

set-status --test BAD_SITE disable
_check BAD_SITE "-2" "0"

set-status --test BAD_SITE ready
_check BAD_SITE "0" "0"

set-status --test TEST_SITE dry
_check TEST_SITE "0" "0"

# Halting should technically only be done for running sites
echo "UPDATE sites SET isrunning=2 WHERE site='TEST_SITE';" | sqlite3 www/stats.db
_check TEST_SITE "2" "0"
set-status --test TEST_SITE halt
_check TEST_SITE "-1" "0"

echo "EC: $ec"

# This should throw an error
set-status --test NOT_SITE ready >& /dev/null
if [ $? -eq 0 ]
then
    ec=$(( $ec + 1 ))
fi

echo "EC: $ec"

# This too
set-status --test TEST_SITE fakeaction >& /dev/null
if [ $? -eq 0 ]
then
    ec=$(( $ec + 1 ))
fi

echo "EC: $ec"

# Check that installation doesn't clobber our database

_check BAD_SITE "0" "0"
_check TEST_SITE "-1" "0"
echo "clobber?"
consistency-web-install --test
_check BAD_SITE "0" "0"
_check TEST_SITE "-1" "0"

exit $ec
