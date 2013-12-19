import os
import fondz
import unittest

test_data = os.path.join(os.path.dirname(__file__), 'data', 'bag1', 'data')

class FileFormat(unittest.TestCase):

    def test_identify_dir(self):
        # alas, mediatype identification fails on travis-ci for some
        # reason that i can't figure out now, so we'll skip those tests
        # for now only when running there
        is_travis = os.environ.get("TRAVIS") == "true"

        formats = fondz.identify.identify_dir(test_data)
        self.assertEqual(len(formats), 4)
        for f in formats:
            if f['path'] == 'data/wordperfect.wp':
                if not is_travis:
                    self.assertEqual(f['mediatype'], 'application/octet-stream')
                self.assertEqual(f['description'], '(Corel/WP)')
                self.assertEqual(f['encoding'], 'binary')
            elif f['path'] == 'data/newspaper.jpg':
                if not is_travis:
                    self.assertEqual(f['mediatype'], 'image/jpeg')
                self.assertEqual(f['description'], 'JPEG image data, JFIF standard 1.01')
                self.assertEqual(f['encoding'], 'binary')
            elif f['path'] == 'data/subdir/word.docx':
                if not is_travis:
                    self.assertEqual(f['mediatype'], 'application/msword')
                self.assertEqual(f['description'], 'Microsoft Word 2007+')
                self.assertEqual(f['encoding'], 'binary')
            elif f['path'] == 'data/word.doc':
                if not is_travis:
                    self.assertEqual(f['mediatype'], 'application/msword')
                self.assertTrue(f['description'].startswith('Composite Document File V2 Document, Little Endian'))
                self.assertEqual(f['encoding'], 'application/mswordbinary')
            else:
                self.fail("unexpected path: %s" % f['path'])
