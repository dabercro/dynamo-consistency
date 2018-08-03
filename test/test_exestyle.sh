#! /bin/bash

errors=0

for f in ../bin/*
do

    pylint $f

    if [ $? -ne 0 ]
    then

        echo "Bad $(basename $f)"
        errors=$(( errors + 1 ))

    fi

done


exit $errors
