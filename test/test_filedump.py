#! /usr/bin/env python

import os
import unittest

import base

from dynamo_consistency.backend.listers import file_reader

class TestFileDump(base.TestBase):
    def test_filedump(self):
        tree = file_reader('filedump.txt', lambda line: (line.split()[0], int(line.split()[2])))

        self.check_equal(self.tree, tree)

if __name__ == '__main__':
    unittest.main()
