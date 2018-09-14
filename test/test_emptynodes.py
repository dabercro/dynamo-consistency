#! /usr/bin/env python

import unittest
import time

import base

class TestEmptyNode(base.TestBase):
    def do_more_setup(self):
        self.tree.get_node('empty').mtime = time.time()
        self.tree.get_node('empty/node').mtime = 1
        self.tree.setup_hash()

    def test_emptyset(self):
        self.assertEqual(len(self.tree.empty_nodes_set()), 1)

if __name__ == '__main__':
    unittest.main()
