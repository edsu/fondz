import os
import json
import fondz
import unittest

test_data = os.path.join(os.path.dirname(__file__), 'data', 'bag1', 'data')


class FileFormat(unittest.TestCase):

    def test_identify_dir(self):
        formats = fondz.identify.identify_dir(test_data)
        self.assertEqual(len(formats), 4)

        # the order of the file formats isn't necessarily determinate
        # also you'll notice some tests test that a value is one of 
        # two options. This is to cover tests on OSX where python-magic
        # results differ in small ways

        for f in formats:
            if f['path'] == 'data/wordperfect.wp':
                self.assertEqual(f['mediatype'], 'application/octet-stream')
                self.assertEqual(f['description'], '(Corel/WP)')
                self.assertTrue(f['encoding'] in ['binary', 'unknown'])
            elif f['path'] == 'data/newspaper.jpg':
                self.assertEqual(f['mediatype'], 'image/jpeg')
                self.assertEqual(f['description'], 'JPEG image data, JFIF standard 1.01')
                # on os x the encoding is uknown for some reason
                self.assertTrue(f['encoding'] in ['binary', 'unknown'])
            elif f['path'] == 'data/subdir/word.docx':
                self.assertTrue(f['mediatype'] in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.documentapplication/zip'])
                self.assertEqual(f['description'], 'Microsoft Word 2007+')
                self.assertTrue(f['encoding'] in ['binary', 'unknown'])
            elif f['path'] == 'data/word.doc':
                self.assertEqual(f['mediatype'], 'application/msword')
                self.assertTrue(f['description'].startswith('Composite Document File V2 Document, Little Endian'))
                self.assertTrue(f['encoding'] in ['application/mswordbinary',
                    'application/mswordunknown'])

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


    def test_summarize(self):
        filename = os.path.join(os.path.dirname(__file__), 'data', 'formats.json')
        f = json.loads(open(filename).read())
        summary = fondz.identify.mediatype_summary(f)
        self.assertEqual(summary[0]['name'], 'text/plain')
        self.assertEqual(len(summary[0]['files']), 8)


