#! /usr/bin/env python

import sys
import time
import logging
import unittest

from ConsistencyCheck import datatypes

class TestFlags(unittest.TestCase):
    new_files = [('/store/yo/0000/file_exists.root', 100, time.time())]
    inventory_files = [('/store/yo/0000/file_exists.root', 100),
                       ('/store/yo/0000/file_not_exists.root', 200)]

    def setUp(self):
        self.remote = datatypes.DirectoryInfo('/store')
        self.remote.add_file_list(self.new_files)
        self.invent = datatypes.DirectoryInfo('/store')
        self.invent.add_file_list(self.inventory_files)

        self.remote.setup_hash()
        self.invent.setup_hash()

    def test_directory_flag(self):
        self.assertFalse(self.remote.get_node('yo/0000').can_compare)

    def test_missing_file(self):
        self.assertEqual(self.invent.compare(self.remote), ([], [], 0))


class TestDate(unittest.TestCase):

    def test_orphan_file(self):
        remote = datatypes.DirectoryInfo('/store')
        remote.add_file_list([('/store/yo/0000/file_exists.root', 100),
                              ('/store/yo/0000/file_not_exists.root', 200, time.time())])
        invent = datatypes.DirectoryInfo('/store')
        invent.add_file_list([('/store/yo/0000/file_exists.root', 100)])
        

        remote.setup_hash()
        invent.setup_hash()

        self.assertEqual(datatypes.compare(invent, remote), ([], 0, [], 0))


class TestSize(unittest.TestCase):

    def test_missing_dir(self):
        remote = datatypes.DirectoryInfo('/store')
        remote.add_file_list([('/store/yo/0000/file_exists.root', 100)])
        invent = datatypes.DirectoryInfo('/store')
        invent.add_file_list([('/store/yo/0000/file_exists.root', 100),
                              ('/store/yo/0000/file_not_exists.root', 100),
                              ('/store/hmm/other/directory.root', 300)])

        remote.setup_hash()
        invent.setup_hash()
        
        self.assertEqual(datatypes.compare(invent, remote)[1], 400)


if __name__ == '__main__':

    if len(sys.argv) > 1:
        logging.basicConfig(level=logging.DEBUG)

    unittest.main()
