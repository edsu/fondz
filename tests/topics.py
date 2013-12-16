import os
import json

from unittest import TestCase

from fondz.topics import topics

test_data = os.path.join(os.path.dirname(__file__), 'data')
keats = os.path.join(test_data, 'keats')

class TopicTest(TestCase):
    
    def test_topics(self):
        t = topics(keats)
        self.assertEqual(len(t), 10)
        self.assertEqual(len(t[0]['words']), 15)

