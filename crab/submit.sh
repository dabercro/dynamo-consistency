#!/bin/bash

SITENAME="$1"
TASKNAME="$2"

if [ -z "$TASKNAME" ]
then
    TASKNAME=$SITENAME
fi

if [ -d "$TASKNAME" ]
then
  echo " This task ($TASKNAME) exists already, please choose other name or remove existing."
  exit 1
else
  bash writeFiles.sh $SITENAME
  crab -create -USER.ui_working_dir $TASKNAME
  if [ "$?" == "0" ]
  then
    crab -submit -c $TASKNAME -GRID.se_white_list=T2_US_MIT
  else
    echo " Task creation failed, look at crab output. Log ($TASKNAME/log/crab.log) has more info."
    exit 1
  fi
fi

exit 0