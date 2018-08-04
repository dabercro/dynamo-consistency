#! /bin/bash

install-consistency-web --test

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

# Check starting status
_check BAD_SITE "-1" "0"   # Only because it's first alphabetically
_check TEST_SITE "0" "0"

exit $ec
