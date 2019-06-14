import os
import sys
import shutil
import unittest

from dynamo_consistency import datatypes

TMP_DIR = 'TempConsistency'

ARGS = [a for a in sys.argv if a not in ['--info', '--debug']]

class TestSimple(unittest.TestCase):
    def setUp(self):
        for dirname in ['www', 'var']:
            if os.path.exists(dirname):
                shutil.rmtree(dirname)
        self.do_more_setup()

    def do_more_setup(self):
        pass


class TestBase(unittest.TestCase):

    file_list = [
        ('/store/mc/ttThings/0000/qwert.root', 20),
        ('/store/mc/ttThings/0000/qwery.root', 30),
        ('/store/mc/ttThings/0001/zxcvb.root', 50),
        ('/store/mc/ttThings/0000/doulb.root', 30),
        ('/store/mc/ttThings/00000/extra_zero.root', 30),
        ('/store/data/runB/earlyfile.root', 5),
        ('/store/data/runB/0001/missi.root', 45),
        ('/store/data/runA/0030/stuff.root', 10),
        ]

    def setUp(self):
        for dirname in ['www', 'var']:
            if os.path.exists(dirname):
                shutil.rmtree(dirname)

        if os.path.exists(TMP_DIR):
            print 'Desired directory location already exists!'
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

        self.assertEqual(tree0.hash, tree1.hash,
                         '\n%s\n=\n%s' % (tree0.displays(), tree1.displays()))
        self.assertEqual([fi['hash'] for fi in tree0._grab_first().files],
                         [fi['hash'] for fi in tree1._grab_first().files])
        self.assertEqual(tree0.get_num_files(), tree1.get_num_files())
        self.assertEqual(tree0.get_num_files(True), tree1.get_num_files(True))



class TestListing(TestBase):

    def do_more_setup(self):
        for name, size in self.file_list:
            path = os.path.join(TMP_DIR, name[7:])
            if not os.path.isdir(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))
            out = open(path, 'w')
            out.write('\0' * size)
            out.close()

            os.utime(path, (1000000000, 1000000000))
