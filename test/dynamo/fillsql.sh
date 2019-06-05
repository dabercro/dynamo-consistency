#! /bin/bash

tar -xf test/dynamo/v1.tgz

# Set up database

cat dump.sql | mysql -ptest

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
);' | mysql -Ddynamoregister -ptest
