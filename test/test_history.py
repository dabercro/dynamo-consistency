#! /usr/bin/env python

import os
import sys
import unittest
import shutil
import sqlite3

from dynamo_consistency import picker
from dynamo_consistency import main
from dynamo_consistency import history
history.config.SITE = 'TEST_SITE_NAME'

class TestHistory(unittest.TestCase):

    missing = [('/store/mc/1/missing.root', 100),
               ('/store/mc/2/missing.root', 2),
               ]

    def setUp(self):
        for dirname in ['www', 'var']:
            if os.path.exists(dirname):
                shutil.rmtree(dirname)

    def tearDown(self):
        history.RUN = None
        history.config.SITE = 'TEST_SITE_NAME'

    def test_run(self):
        history.start_run()
        self.assertTrue(history.RUN)
        history.finish_run()
        self.assertFalse(history.RUN)

    def test_missing(self):
        history.start_run()
        history.report_missing(self.missing)
        history.finish_run()

        self.assertEqual(history.missing_files(history.config.SITE),
                         sorted([miss[0] for miss in self.missing]))


    def test_two_sites(self):
        missing2 = [('/store/mc/4/missing.root', 2),
                    ('/store/mc/3/missing.root', 100),
                    ]

        history.start_run()
        history.report_missing(self.missing)
        history.finish_run()
        history.config.SITE = 'TEST_SITE_NAME_2'
        history.start_run()
        history.report_missing(missing2)
        history.finish_run()

        history.config.SITE = 'TEST_SITE_NAME'

        self.assertEqual(history.missing_files('TEST_SITE_NAME'),
                         sorted([miss[0] for miss in self.missing]))

        self.assertEqual(history.missing_files('TEST_SITE_NAME_2'),
                         sorted([miss[0] for miss in missing2]))

    def test_two_runs(self):
        missing2 = [('/store/mc/4/missing.root', 2),
                    ('/store/mc/3/missing.root', 100),
                    ]

        history.start_run()
        history.report_missing(self.missing)
        history.finish_run()
        history.start_run()
        history.report_missing(missing2)
        history.finish_run()

        self.assertEqual(history.missing_files('TEST_SITE_NAME'),
                         sorted([miss[0] for miss in missing2]))

    def test_acting(self):
        history.start_run()
        history.report_missing(self.missing)
        history.finish_run()

        self.assertEqual(history.missing_files(history.config.SITE, False),
                         sorted([miss[0] for miss in self.missing]))

        self.assertEqual(history.missing_files(history.config.SITE, True),
                         sorted([miss[0] for miss in self.missing]))

        self.assertFalse(history.missing_files(history.config.SITE))

    def test_siteunique(self):
        history.start_run()
        history.finish_run()
        history.start_run()
        history.finish_run()

        conn, curs = history._connect()

        curs.execute('SELECT * FROM sites;')

        result = list(curs.fetchall())

        conn.close()

        self.assertEqual(len(result), 1)

    def test_orphan(self):
        history.start_run()
        history.report_orphan(self.missing)
        history.finish_run()

        self.assertEqual(history.orphan_files(history.config.SITE),
                         sorted([miss[0] for miss in self.missing]))

        self.assertFalse(history.missing_files(history.config.SITE))

    def test_unmerged(self):
        history.start_run()
        history.report_unmerged(self.missing)
        history.finish_run()

        self.assertEqual(history.unmerged_files(history.config.SITE),
                         sorted([miss[0] for miss in self.missing]))

        self.assertFalse(history.missing_files(history.config.SITE))

    def test_main(self):
        main.main(picker.pick_site())

        self.assertFalse(history.RUN)

        # See dynamo_consistency.backend.test for expected results

        self.assertEqual(history.missing_files(main.config.SITE),
                         ['/store/data/runB/0003/missing.root'])
        self.assertEqual(history.orphan_files(main.config.SITE),
                         ['/store/data/runB/0001/orphan.root'])
        self.assertEqual(history.emtpy_directories(main.config.SITE),
                         ['/store/data/runC/0000/emtpy/dir',
                          '/store/data/runC/0000/emtpy',
                          '/store/data/runC/0000',
                          '/store/data/runC'])


if __name__ == '__main__':
    unittest.main(argv=[a for a in sys.argv if a not in ['--info', '--debug']])
