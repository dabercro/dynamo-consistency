#! /usr/bin/env python

import sys
import unittest

sys.argv.append('watch')

import logger

class TestWatch(logger.TestLogger):
    pass

if __name__ == '__main__':
    unittest.main(argv=[a for a in sys.argv if a not in ['watch', 'debug']])
