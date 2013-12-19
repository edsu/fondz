import os
import fondz
import unittest

test_data = os.path.join(os.path.dirname(__file__), 'data', 'bag1', 'data')

class FileFormat(unittest.TestCase):

    def test_mediatype(self):
        f = os.path.join(test_data, 'word.doc')
        mt = fondz.identify.mediatype(f)
        self.assertEqual(mt, 'application/msword')

    def test_identify_dir(self):
        formats = fondz.identify.identify_dir(test_data)
        self.assertEqual(len(formats), 4)
        for f in formats:
            if f['path'] == 'data/wordperfect.wp':
                #self.assertEqual(f['mediatype'], 'application/octet-stream')
                self.assertEqual(f['description'], '(Corel/WP)')
            elif f['path'] == 'data/newspaper.jpg':
                #self.assertEqual(f['mediatype'], 'image/jpeg')
                self.assertEqual(f['description'], 'JPEG image data, JFIF standard 1.01')
            elif f['path'] == 'data/subdir/word.docx':
                #self.assertEqual(f['mediatype'], 'application/msword')
                self.assertEqual(f['description'], 'Microsoft Word 2007+')
            elif f['path'] == 'data/word.doc':
                #self.assertEqual(f['mediatype'], 'application/msword')
                self.assertTrue(f['description'].startswith('Composite Document File V2 Document, Little Endian'))
            else:
                self.fail("unexpected path: %s" % f['path'])
