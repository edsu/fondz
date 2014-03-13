import os
import tempfile
import fondz
import unittest

from os.path import join, dirname, isfile, getsize
from fondz.create import add_bag
from fondz.convert import convert_to_html, convert

bag1 = join(dirname(__file__), 'data', 'bag1', 'data')
bag3 = join(dirname(__file__), 'data', 'bag3', 'data')

class ConvertTest(unittest.TestCase):

    def test_wordperfect(self):
        f1 = join(bag1, 'wordperfect.wp')
        f2 = convert_to_html(f1)
        self.assertTrue(f2)
        self.assertTrue(isfile(f2))

    def test_word(self):
        f1  = join(bag1, 'word.doc')
        f2 = convert_to_html(f1)
        self.assertTrue(f2)
        self.assertTrue(isfile(f2))
        self.assertTrue(getsize(f2) > 0)

    def test_pdf(self):
        f1 = join(bag3, 'w2g_13.pdf')
        f2 = convert_to_html(f1)
        self.assertTrue(f2)
        self.assertTrue(isfile(f2))
        # obviously incomplete, but hopefully makes sure it's roughly working
        self.assertTrue("receiving the winnings" in open(f2).read())

    def test_convert(self):
        target_dir = tempfile.mkdtemp() 
        convert(bag1, target_dir)
        files = os.listdir(target_dir)
        self.assertEqual(len(files), 3)
        self.assertTrue('word.doc.html' in files)
        self.assertTrue('wordperfect.wp.html' in files)
        self.assertTrue('subdir' in files)
        subdir = join(target_dir, 'subdir')
        files = os.listdir(subdir)
        self.assertEqual(len(files), 1)
        self.assertTrue('word.docx.html' in files)
