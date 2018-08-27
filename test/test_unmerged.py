#! /usr/bin/env python

# Test the unmerged configuration

import os
import sys
import unittest

from dynamo_consistency.cms import unmerged
from dynamo_consistency.backend.test import TMP_DIR
from dynamo_consistency.backend import registry

import base


unmerged.listdeletable.get_protected = lambda: [
    '/store/unmerged/protected',
    '/store/unmerged/protected2'
    ]


class TestUnmerged(base.TestListing):
    file_list = [
        ('/store/unmerged/protected/000/qwert.root', 20),
        ('/store/unmerged/notprot/000/qwert.root', 20),
        ('/store/unmerged/logs/000/logfile.tar.gz', 20)
        ]

    dir_list = [
        '/store/unmerged/protected/empty',
        '/store/unmerged/protected2',
        ]

    def do_more_setup(self):
        super(TestUnmerged, self).do_more_setup()

        for name in self.dir_list:
            path = os.path.join(TMP_DIR, name[7:])
            if not os.path.exists(path):
                os.makedirs(path)

    def test_deletion_file(self):
        unmerged.clean_unmerged('test')


class TestSetup(unittest.TestCase):
    def test_tmpdir(self):
        # Make sure these are the same
        self.assertEqual(TMP_DIR, base.TMP_DIR)


if __name__ == '__main__':
    unittest.main(argv=[a for a in sys.argv if a not in ['--info', '--debug']])
