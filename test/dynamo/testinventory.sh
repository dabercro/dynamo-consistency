#! /bin/bash

# Only run where dynamo is installed
which dynamo || exit 0

cd `dirname $0`
tarball=$PWD/v1.tgz

cd /work || exit 1

# Assume we're inside a Docker container
mkdir -p var/cache/T3_US_MIT

tar -xf $tarball

mv remote.pkl var/cache/T3_US_MIT

cat dump.sql | mysql
