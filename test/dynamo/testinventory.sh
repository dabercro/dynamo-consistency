#! /bin/bash

# Only run where dynamo is installed
which dynamo || exit 0

cd `dirname $0`
tarball=$PWD/v1.tgz
conf=$PWD/consistency_config.json
check=$PWD/checkhistory.py

cd /work || exit 1

# Assume we're inside a Docker container
mkdir -p var/cache/T3_US_MIT

tar -xf $tarball

mv remote.pkl var/cache/T3_US_MIT

cat dump.sql | mysql

echo '
CREATE TABLE `deletion_queue` (
  `reqid` int(10) unsigned NOT NULL DEFAULT "0",
  `file` varchar(512) COLLATE latin1_general_cs NOT NULL,
  `site` varchar(32) COLLATE latin1_general_cs NOT NULL,
  `status` enum("new","done","failed") COLLATE latin1_general_cs NOT NULL,
  UNIQUE KEY `file` (`file`,`site`)
);
CREATE TABLE `transfer_queue` (
  `reqid` int(10) unsigned NOT NULL,
  `file` varchar(512) COLLATE latin1_general_cs NOT NULL,
  `site_from` varchar(32) COLLATE latin1_general_cs NOT NULL,
  `site_to` varchar(32) COLLATE latin1_general_cs NOT NULL,
  `status` enum("new","done","failed") COLLATE latin1_general_cs NOT NULL,
  UNIQUE KEY `file` (`file`,`site_from`,`site_to`)
);
' | mysql -D dynamoregister

dynamo "`which dynamo-consistency` --site T3_US_MIT --info --v1 --config $conf" || exit 4

$check || exit 2

# Check inventory object use
dynamo "`which dynamo-consistency` --site T3_US_MIT --info --config $conf" || exit 5

$check || exit 3
