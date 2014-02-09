import os
import tempfile
import fondz
import unittest

from os.path import join, dirname, isfile, getsize
from fondz.create import init, add_bag
from fondz.convert import convert_to_html, convert

bag1 = join(dirname(__file__), 'data', 'bag1')
test_data = join(bag1, 'data')

class ConvertTest(unittest.TestCase):

    def test_wordperfect(self):
        f1 = join(test_data, 'wordperfect.wp')
        f2 = convert_to_html(f1)
        self.assertTrue(f2)
        self.assertTrue(isfile(f2))

    def test_word(self):
        f1  = join(test_data, 'word.doc')
        f2 = convert_to_html(f1)
        self.assertTrue(f2)
        self.assertTrue(isfile(f2))
        self.assertTrue(getsize(f2) > 0)

    def test_convert(self):
        target_dir = tempfile.mkdtemp() 
        convert(test_data, target_dir)
        files = os.listdir(target_dir)
        self.assertEqual(len(files), 3)
        self.assertTrue('word.doc.html' in files)
        self.assertTrue('wordperfect.wp.html' in files)
        self.assertTrue('subdir' in files)
        subdir = join(target_dir, 'subdir')
        files = os.listdir(subdir)
        self.assertEqual(len(files), 1)
        self.assertTrue('word.docx.html' in files)
