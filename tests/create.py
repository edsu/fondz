import os
import tempfile
import unittest

from fondz import create

bag1 = os.path.join(os.path.dirname(__file__), 'data', 'bag1')

class CreateTests(unittest.TestCase):

    def test_create(self):
        d = tempfile.mkdtemp()
        create(d, bag1)
        self.assertTrue(os.path.isdir(d))
        index = os.path.join(d, "index.html")
        self.assertTrue(os.path.isfile(index))

