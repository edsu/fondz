import json
import uuid
import fondz
import tempfile
import unittest

from fondz.create import init, add_bag, create
from fondz.utils import read_json

from os.path import join, isdir, dirname, isfile, islink, realpath, getsize

bag1 = join(dirname(__file__), 'data', 'bag1')
bag2 = join(dirname(__file__), 'data', 'bag2')

class CreateTests(unittest.TestCase):

    def test_init(self):
        d = tempfile.mkdtemp()
        init("test", d)
        self.assertTrue(isdir(join(d, "derivatives")))
        self.assertTrue(isfile(join(d, "fondz.json")))

        log_file = join(d, "fondz.log")
        self.assertTrue(isfile(log_file))
        self.assertTrue(getsize(log_file) > 0)

    def test_add_bags(self):
        # create a fondz directory, and add 2 test bags to it
        fondz_dir = tempfile.mkdtemp()
        init("test", fondz_dir)
        add_bag(fondz_dir, bag1)
        add_bag(fondz_dir, bag2)

        # generate and load fondz.js
        fondz_json = join(fondz_dir, "fondz.json")
        self.assertTrue(isfile(fondz_json))
        result = read_json(fondz_json)

        # check that bags are there
        self.assertEqual(len(result['bags']), 2)
        self.assertEqual(result['num_files'], 12)
        self.assertEqual(result['bytes'], 7772330)
        self.assertEqual(result['bags'][0]['path'], bag1)
        self.assertEqual(len(result['bags'][0]['manifest']), 4)
        self.assertEqual(result['bags'][1]['path'], bag2)
        self.assertEqual(len(result['bags'][1]['manifest']), 8)

        # look closer at bag1
        self.assertTrue(uuid.UUID(result['bags'][0]['id']))
        f = result['bags'][0]['manifest'][0]
        self.assertEqual(f['path'], 'data/newspaper.jpg')
        self.assertEqual(f['md5'], 'a0471d984e6e82f15da686cebdb38a36')
        self.assertEqual(f['bytes'], 7004510)
        self.assertTrue(f['modified'])
        self.assertTrue(f['created'])
        self.assertEqual(f['format'], 'fmt/43')

        # make sure formats are populated
        self.assertEqual(len(result['formats'].keys()), 5)

        # make at least one derivative is there
        bag_id = result['bags'][0]['id']
        f = result['bags'][0]['manifest'][1]

        deriv = join(fondz_dir, 'derivatives', bag_id, 'word.doc.html')
        self.assertTrue(isfile(deriv))

    def test_create(self):
        d = tempfile.mkdtemp()
        create("test", d, bag1, overwrite=True)
        self.assertTrue(isdir(d))

        # fondz.json there?
        fondz_file = join(d, "fondz.json")
        self.assertTrue(isfile(fondz_file))
        fondz = read_json(fondz_file)
        bag_id = fondz["bags"][0]["id"]

        # topics there
        self.assertTrue(len(fondz["topic_model"]["topics"]) > 0)

        # bag is there
        self.assertEqual(len(fondz['bags']), 1)
        self.assertEqual(fondz['bags'][0]['path'], bag1)
        self.assertEqual(len(fondz['bags'][0]['manifest']), 4)

        f = fondz['bags'][0]['manifest'][0]
        self.assertEqual(f['path'], 'data/newspaper.jpg')
        self.assertEqual(f['bytes'], 7004510)
        self.assertEqual(f['format'], 'fmt/43')

        f = fondz['bags'][0]['manifest'][1]
        self.assertEqual(f['path'], 'data/wordperfect.wp')
        self.assertEqual(f['bytes'], 672936)
        self.assertEqual(f['format'], 'x-fmt/394')

        self.assertTrue(isfile(join(d, "derivatives", bag_id, "word.doc.html")))
        self.assertTrue(isfile(join(d, "derivatives", bag_id, "wordperfect.wp.html")))
        self.assertTrue(isfile(join(d, "derivatives", bag_id, "subdir", "word.docx.html")))

        # html files there?
        for f in ["index.html", "topics.html", "formats.html", "bags.html"]:
            html_file = join(d, f)
            self.assertTrue(isfile(html_file))
            html = open(html_file).read()
            self.assertTrue('<!doctype html>' in html)


def isjson(filename):
    return json.loads(open(filename).read())
