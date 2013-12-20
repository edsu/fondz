import os
import fondz
import unittest

test_data = os.path.join(os.path.dirname(__file__), 'data', 'bag1', 'data')


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


    def test_symlink(self):
        link_name = 'test__symlink'
        if os.path.islink(link_name):
            os.remove(link_name)
        os.symlink(test_data, link_name)
        formats = fondz.identify.identify_dir(link_name)
        self.assertEqual(len(formats), 4)
        os.remove(link_name)
