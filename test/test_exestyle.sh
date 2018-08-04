#! /bin/bash

pylint --disable=invalid-name,broad-except --ignored-modules=dynamo_consistency.opts ../bin/*

exit $?
