#! /usr/bin/env python

"""
Jobs of datatypes:

- Define a tree type that can be quickly compared with other trees
- Save the tree without data loss
- Remote listing and using a local list to check consistency
- In the tree, files that are too new should not affect the comparison

Things to test:

x Save and load trees and compare them to trees only in memory
- Creation of tree through list of files and through a filler function
  and compare them to see if they're the same
- Create two different trees and make sure the differences noted are correct
- Create new files and see if they affect the hash
- Create multiple trees and merge them
"""

import os
import time
import shutil
import unittest

from ConsistencyCheck import config
from ConsistencyCheck import datatypes


WAIT = config.config_dict()['IgnoreAge'] * 24 * 3600
TMP_DIR = 'TempConsistency'

# Define a filler function to use in the "remote filling" test
def my_ls(path):

    results = os.listdir(os.path.join(TMP_DIR, path))
    return filter(os.path.isdir, results), filter(os.path.isfile, results)

class TestBase(unittest.TestCase):

    tree = None
    tmpdir = None

    file_list = [
        ('/store/mc/ttThings/0000/qwert.root', 20),
        ('/store/mc/ttThings/0000/qwery.root', 30),
        ('/store/mc/ttThings/0001/zxcvb.root', 50),
        ('/store/mc/ttThings/0000/doulb.root', 30),
        ('/store/data/runB/0001/missi.root', 45),
        ('/store/data/runA/0030/stuff.root', 10),
        ]

    def setUp(self):
        if os.path.exists(TMP_DIR):
            print 'Desire directory location already exists!'
            exit(1)
        os.makedirs(TMP_DIR)
        self.tree = datatypes.DirectoryInfo('/store')
        self.tree.add_file_list(self.file_list)
        self.do_more_setup()

    def tearDown(self):
        if os.path.exists(TMP_DIR):
            shutil.rmtree(TMP_DIR)

    def do_more_setup(self):
        pass

    def check_equal(self, tree0, tree1):

        tree0.setup_hash()
        tree1.setup_hash()

        print '='*30
        tree0.display()
        print '='*30
        tree1.display()

        self.assertEqual(tree0.hash, tree1.hash)
        self.assertEqual(tree0._grab_first().files,
                         tree1._grab_first().files)


class TestTree(TestBase):

    def test_do_hash(self):
        self.assertFalse(self.tree.hash)
        self.tree.setup_hash()
        self.assertTrue(self.tree.hash)

    def test_compare_saved(self):
        self.tree.save(os.path.join(TMP_DIR, 'tree.pkl'))
        tree0 = datatypes.get_info(os.path.join(TMP_DIR, 'tree.pkl'))

        self.check_equal(self.tree, tree0)

    def test_merge_trees(self):
        trees = {
            'mc': datatypes.DirectoryInfo('mc'),
            'data': datatypes.DirectoryInfo('data')
            }

        for key, tree in trees.iteritems():
            tree.add_file_list([('/'.join(name.split('/')[2:]), size) \
                                    for name, size in self.file_list if name.split('/')[2] == key])

        one_tree = datatypes.DirectoryInfo('/store', [trees['data'], trees['mc']])
        self.check_equal(self.tree, one_tree)

        # Hopefully order doesn't matter

        two_tree = datatypes.DirectoryInfo('/store', [trees['mc'], trees['data']])
        self.check_equal(self.tree, two_tree)
        self.check_equal(one_tree, two_tree)

class TestConsistentTrees(TestBase):

    def do_more_setup(self):
        for name, size in self.file_list:
            out = open(os.path.join(TMP_DIR, name[7:]), 'r')
            out.write(bytearray(os.urandom(size)))
            out.close()

        time.sleep(WAIT * 1.5)


class TestInconsistentTrees(TestBase):

    orphan = [
        ('/store/data/runE/0000/toomany.root', 20)
        ]
    missing = [
        ('/store/mc/Zllll/0023/signal.root', 15)
        ]

if __name__ == '__main__':
    unittest.main()