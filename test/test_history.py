#! /usr/bin/env python

import os
import unittest

from dynamo_consistency import history
history.config.SITE = 'TEST_SITE_NAME'

class TestHistory(unittest.TestCase):

    missing = [('/store/mc/1/missing.root', 100),
               ('/store/mc/2/missing.root', 2),
               ]

    def setUp(self):
        db = 'var/db/consistency.db'
        if os.path.exists(db):
            os.remove(db)

    def tearDown(self):
        history.RUN = None

    def test_run(self):
        history.start_run()
        self.assertTrue(history.RUN)
        history.finish_run()
        self.assertFalse(history.RUN)

    def test_missing(self):
        self.assertRaises(history.NotRunning,
                          history.report_missing, self.missing)

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

    def test_acting(self):
        history.start_run()
        history.report_missing(self.missing)
        history.finish_run()

        self.assertEqual(history.missing_files(history.config.SITE, False),
                         sorted([miss[0] for miss in self.missing]))

        self.assertEqual(history.missing_files(history.config.SITE, True),
                         sorted([miss[0] for miss in self.missing]))

        self.assertFalse(history.missing_files(history.config.SITE))



if __name__ == '__main__':
    unittest.main()
