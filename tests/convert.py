import os
import tempfile
from unittest import TestCase

from fondz.convert import convert_dir, convert_to_html

test_data = os.path.join(os.path.dirname(__file__), 'data', 'bag1', 'data')

class ConvertTest(TestCase):

    def test_wordperfect(self):
        f1 = os.path.join(test_data, 'wordperfect.wp')
        f2 = convert_to_html(f1)
        self.assertTrue(f2)
        self.assertTrue(os.path.isfile(f2))

    def test_word(self):
        f1  = os.path.join(test_data, 'word.doc')
        f2 = convert_to_html(f1)
        self.assertTrue(f2)
        self.assertTrue(os.path.isfile(f2))

    def test_convert_dir(self):
        target_dir = tempfile.mkdtemp() 
        convert_dir(test_data, target_dir)
        files = os.listdir(target_dir)
        self.assertEqual(len(files), 3)
        self.assertTrue('word.doc.html' in files)
        self.assertTrue('wordperfect.wp.html' in files)
        self.assertTrue('subdir' in files)
        subdir = os.path.join(target_dir, 'subdir')
        files = os.listdir(subdir)
        self.assertEqual(len(files), 1)
        self.assertTrue('word.docx.html' in files)


