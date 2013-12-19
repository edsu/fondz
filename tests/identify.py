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
                self.assertEqual(f['mediatype'], 'application/octet-stream')
                self.assertEqual(f['description'], '(Corel/WP)')
            elif f['path'] == 'data/newspaper.jpg':
                self.assertEqual(f['mediatype'], 'image/jpeg')
                self.assertEqual(f['description'], 'JPEG image data, JFIF standard 1.01')
            elif f['path'] == 'data/subdir/word.docx':
                self.assertEqual(f['mediatype'], 'application/msword')
                self.assertEqual(f['description'], 'Microsoft Word 2007+')
            elif f['path'] == 'data/word.doc':
                self.assertEqual(f['mediatype'], 'application/msword')
                self.assertEqual(f['description'], "Composite Document File V2 Document, Little Endian, Os: Windows, Version 5.0, Code page: 1252, Title: _, Template: Normal.dot, Last Saved By:  , Revision Number: 6, Name of Creating Application: Microsoft Word 10.0, Last Printed: Wed Aug 24 20:41:00 2005, Create Time/Date: Thu Aug 25 20:50:00 2005, Last Saved Time/Date: Thu Aug 25 20:54:00 2005, Number of Pages: 2, Number of Words: 297, Number of Characters: 1648, Security: 0")
            else:
                self.fail("unexpected path: %s" % f['path'])
