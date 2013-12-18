import os
import json

from unittest import TestCase

from fondz.topics import topics

test_data = os.path.join(os.path.dirname(__file__), 'data', 'bag2', 'data')

class TopicTest(TestCase):
    
    def test_topics(self):
        t = topics(test_data)
        self.assertEqual(len(t), 10)
        self.assertEqual(len(t[0]['words']), 15)

