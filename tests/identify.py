import os
import fondz
import unittest

test_data = os.path.join(os.path.dirname(__file__), 'data', 'bag1', 'data')
is_travis = os.environ.get("TRAVIS") == "true"

# unfortunately format identification tests are unprecitable on travis-ci
# probably because of something weird in the environment and libmagic1 
# so we don't run these tests on there

@unittest.skipIf(is_travis)
class FileFormat(unittest.TestCase):

    def test_identify_dir(self):
        formats = fondz.identify.identify_dir(test_data)
        self.assertEqual(len(formats), 4)

        # the order of the file formats isn't necessarily determinate
        for f in formats:
            if f['path'] == 'data/wordperfect.wp':
                self.assertEqual(f['mediatype'], 'application/octet-stream')
                self.assertEqual(f['description'], '(Corel/WP)')
                self.assertEqual(f['encoding'], 'binary')
            elif f['path'] == 'data/newspaper.jpg':
                self.assertEqual(f['mediatype'], 'image/jpeg')
                self.assertEqual(f['description'], 'JPEG image data, JFIF standard 1.01')
                self.assertEqual(f['encoding'], 'binary')
            elif f['path'] == 'data/subdir/word.docx':
                self.assertEqual(f['mediatype'], 'application/msword')
                self.assertEqual(f['description'], 'Microsoft Word 2007+')
                self.assertEqual(f['encoding'], 'binary')
            elif f['path'] == 'data/word.doc':
                self.assertEqual(f['mediatype'], 'application/msword')
                self.assertTrue(f['description'].startswith('Composite Document File V2 Document, Little Endian'))
                self.assertEqual(f['encoding'], 'application/mswordbinary')
            else:
                self.fail("unexpected path: %s" % f['path'])
