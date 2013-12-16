import os
import tempfile
from unittest import TestCase

from fondz.convert import convert, convert_to_html

test_data = os.path.join(os.path.dirname(__file__), 'data', 'convert')

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





