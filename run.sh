#!/bin/bash

here=`pwd`

cd ${0%%`basename $0`}

nohup ./RunCheck.sh > $ConsistencyCacheDirectory/nohup_`date +%y%m%d`.out 2>&1&

cd $here