#! /usr/bin/env python

import os
import sys
import unittest
import logging
import glob
import shutil

from dynamo_consistency import logsetup

class TestLogger(unittest.TestCase):
    def setUp(self):
        # Will only work if empty
        if os.path.exists('logs'):
            os.rmdir('logs')


    def tearDown(self):

        for logger in logging.Logger.manager.loggerDict.values():
            hdlr_copy = list(logger.handlers)
            for hdlr in hdlr_copy:
                logger.removeHandler(hdlr)

        for f in glob.glob('logs/*'):
            print f
            with open(f, 'r') as fh:
                for line in fh:
                    print line.strip()
            os.remove(f)


    def write_files(self, num_1, num_2):
        # Number of lines that should be in 1 and 2
        # This will include all levels
        test1 = logging.getLogger('test1')
        test2 = logging.getLogger('test2')

        self.assertFalse(os.path.exists('logs'))
        logsetup.change_logfile('logs/test1.log')

        self.assertTrue(os.path.exists('logs'))
        test1.debug('First debug')
        test1.info('First info')
        test1.warning('First warning')

        logsetup.change_logfile('logs/test2.log')

        test1.debug('Second debug')
        test1.info('Second info')
        test1.warning('Second warning')

        test2.debug('Third debug')
        test2.info('Third info')
        test2.warning('Third warning')

        logsetup.change_logfile('logs/test3.log', 'logs/test4.log')

        test1.warning('Fourth warning')

        logsetup.change_logfile('logs/test4.log')

        test2.warning('Fifth warning')

        with open('logs/test1.log', 'r') as lfile:
            self.assertEqual(len(list(lfile)), num_1)

        with open('logs/test2.log', 'r') as lfile:
            self.assertEqual(len(list(lfile)), num_2)

        with open('logs/test3.log', 'r') as lfile:
            self.assertEqual(len(list(lfile)), 1)

        with open('logs/test4.log', 'r') as lfile:
            self.assertEqual(len(list(lfile)), 2)


    def test_writing(self):
        mult = 1
        if '--debug' in sys.argv:
            mult = 3
        elif '--info' in sys.argv:
            mult = 2

        self.write_files(mult, mult * 2)
