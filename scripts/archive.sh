#! /bin/bash

FROM=$1  # First argument is the location of our consistency var directory
TO=$2    # Second argument is the directory where we store all of the files

cd $FROM || exit 1

# We will run this weekly to gather things older than 2 weeks, so date this from 3 to 2 weeks ago
TARNAME=consistency_$(date --date="3 weeks ago" +%y%m%d)_$(date --date="2 weeks ago" +%y%m%d)

# Create destination directory if it doesn't exist
if [ ! -d $TO ]
then
    mkdir -p $TO || exit 2
fi

# Create directory to hold what we want
mkdir $TARNAME || exit 3

# Move file into $TARNAME with same relative path
bigmv () {

    NAME=$1

    # Make target directory for move if needed
    TARGET=$(dirname $TARNAME/$NAME)
    if [ ! -d $TARGET ]
    then
        mkdir -p $TARGET || exit 4
    fi

    mv $NAME $TARGET || exit 5

}

# Move everything older than 14 days in
# "cache" and "logs" directories to make tarball
for f in $(find cache logs -type f -mtime +14)
do
    bigmv $f
done

# Create tarball
tar -czf $TARNAME.tgz $TARNAME || exit 6
# Don't overwrite if file there
test ! -f $TO/$TARNAME.tgz || exit 7
# Move it to destination
mv $TARNAME.tgz $TO || exit 8

# Clear up old files
rm -rf $TARNAME || exit 9
