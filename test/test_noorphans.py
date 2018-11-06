#! /usr/bin/env python

import os
import shutil
import sys
import unittest

import base

# Set the NOORPHAN flag
import dynamo_consistency
dynamo_consistency.opts.NOORPHAN = True

from dynamo_consistency import main
from dynamo_consistency import picker
from dynamo_consistency import history

class TestNoOrphan(unittest.TestCase):
    def setUp(self):
        for dirname in ['www', 'var']:
            if os.path.exists(dirname):
                shutil.rmtree(dirname)

    def test_main(self):
        main.main(picker.pick_site())

        self.assertEqual(history.missing_files(main.config.SITE),
                         ['/store/data/runB/0003/missing.root'])
        self.assertFalse(history.orphan_files(main.config.SITE))
        self.assertEqual(history.emtpy_directories(main.config.SITE),
                         ['/store/data/runC/0000/emtpy/dir',
                          '/store/data/runC/0000/emtpy',
                          '/store/data/runC/0000',
                          '/store/data/runC'])

        self.assertEqual(sorted(main.registry.deleted, reverse=True),
                         history.emtpy_directories(main.config.SITE))


if __name__ == '__main__':
    unittest.main(argv=base.ARGS)
