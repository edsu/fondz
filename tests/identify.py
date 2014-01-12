import os
import json
import fondz
import shutil
import tempfile
import unittest

test_data = os.path.join(os.path.dirname(__file__), 'data', 'bag1', 'data')


class FileFormat(unittest.TestCase):

    def test_identify(self):
        fondz_dir = tempfile.mkdtemp()
        fondz.create.init(fondz_dir)

        bag1 = os.path.join(os.path.dirname(__file__), 'data', 'bag1')
        fondz.create.add_bag(fondz_dir, bag1)

        bag2 = os.path.join(os.path.dirname(__file__), 'data', 'bag2')
        fondz.create.add_bag(fondz_dir, bag2)

        results = fondz.identify.identify(fondz_dir)
        self.assertEqual(len(results), 12)

        # make sure all the paths have been made relative
        for f in results:
            self.assertTrue(f['path'].startswith('originals'))

        shutil.rmtree(fondz_dir)

    def test_identify_dir(self):
        formats = fondz.identify.identify_dir(test_data)
        self.assertEqual(len(formats), 4)

        formats.sort(lambda a, b: cmp(a['mediatype'], b['mediatype']))

        self.assertTrue(os.path.isfile(formats[0]['path']))
        self.assertEqual(formats[0]['mediatype'], 'None')
        self.assertEqual(formats[0]['name'], 'Microsoft Office Open XML - Word')
        self.assertEqual(formats[0]['description'], 'Microsoft Office Open XML - Word')


        self.assertTrue(os.path.isfile(formats[1]['path']))
        self.assertEqual(formats[1]['mediatype'], 'application/msword')
        self.assertEqual(formats[1]['name'], 'Microsoft Word for Windows Document')
        self.assertEqual(formats[1]['description'], 'Microsoft Word for Windows 97 - 2002')

        self.assertTrue(os.path.isfile(formats[2]['path']))
        self.assertEqual(formats[2]['mediatype'], 'application/vnd.wordperfect')
        self.assertEqual(formats[2]['name'], 'WordPerfect for MS-DOS/Windows Document')
        self.assertEqual(formats[2]['description'], 'WordPerfect 5.1')

        self.assertTrue(os.path.isfile(formats[3]['path']))
        self.assertEqual(formats[3]['mediatype'], 'image/jpeg')
        self.assertEqual(formats[3]['name'], 'JPEG File Interchange Format')
        self.assertEqual(formats[3]['description'], 'JFIF 1.01')


    def test_summarize(self):
        filename = os.path.join(os.path.dirname(__file__), 'data', 'formats.json')
        f = json.loads(open(filename).read())
        summary = fondz.identify.mediatype_summary(f)
        self.assertEqual(summary[0]['name'], 'text/plain')
        self.assertEqual(len(summary[0]['files']), 8)
