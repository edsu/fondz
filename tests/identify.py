import json
import fondz
import shutil
import tempfile
import unittest

from os.path import join, dirname
from fondz.create import init, add_bag
from fondz.identify import get_file_formats

test_data = join(dirname(__file__), 'data', 'bag1')


class FileFormatTest(unittest.TestCase):

    def test_get_file_formats(self):
        files, formats = get_file_formats(test_data)

        self.assertEqual(len(files.keys()), 4)
        self.assertEqual(len(formats.keys()), 4)

        self.assertEqual(files["data/subdir/word.docx"], "fido-fmt/189.word")
        self.assertEqual(files["data/wordperfect.wp"], "x-fmt/394")
        self.assertEqual(files["data/newspaper.jpg"], "fmt/43")
        self.assertEqual(files["data/word.doc"], "fmt/40")

        self.assertEqual(formats["x-fmt/394"]["name"],
            "WordPerfect for MS-DOS/Windows Document")
        self.assertEqual(formats["x-fmt/394"]["mediatype"],
            "application/vnd.wordperfect")
        self.assertEqual(formats["x-fmt/394"]["description"],
            "WordPerfect 5.1")

        self.assertEqual(formats["fido-fmt/189.word"]["name"],
            "Microsoft Office Open XML - Word")
        self.assertEqual(formats["fido-fmt/189.word"]["mediatype"], 'None')
        self.assertEqual(formats["fido-fmt/189.word"]["description"],
            'Microsoft Office Open XML - Word')

        self.assertEqual(formats["fmt/43"]["name"],
            "JPEG File Interchange Format")
        self.assertEqual(formats["fmt/43"]["description"], "JFIF 1.01")
        self.assertEqual(formats["fmt/43"]["mediatype"], "image/jpeg")

        self.assertEqual(formats["fmt/40"]["name"],
            "Microsoft Word for Windows Document")
        self.assertEqual(formats["fmt/40"]["mediatype"], "application/msword")
        self.assertEqual(formats["fmt/40"]["description"],
            "Microsoft Word for Windows 97 - 2002")
