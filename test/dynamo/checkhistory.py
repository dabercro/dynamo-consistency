#! /usr/bin/env python

from dynamo_consistency import history

if __name__ == '__main__':
    if len(history.orphan_files('T3_US_MIT')) != 2:
        exit (1)
    if len(history.missing_files('T3_US_MIT')):
        exit (2)
