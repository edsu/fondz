import os
import fondz
import tempfile
import unittest

from fondz.utils import read_json
from fondz.create import init, add_bag


bag1 = os.path.join(os.path.dirname(__file__), 'data', 'bag1')
bag2 = os.path.join(os.path.dirname(__file__), 'data', 'bag2')

class BagsTests(unittest.TestCase):

    def test_bags(self):
        fondz_dir = tempfile.mkdtemp()
        init(fondz_dir)
        add_bag(fondz_dir, bag1)
        add_bag(fondz_dir, bag2)
        fondz.bags(fondz_dir)

        bags_json = os.path.join(fondz_dir, "js", "bags.json")
        self.assertTrue(os.path.isfile(bags_json))
        result = read_json(bags_json)
        self.assertEqual(len(result['bags']), 2)
        self.assertEqual(result['num_files'], 12)
        self.assertEqual(result['bytes'], 7772330)



