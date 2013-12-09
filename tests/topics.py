import os

from unittest import TestCase

import diagnidnif

test_data = os.path.join(os.path.dirname(__file__), 'data')
keats = os.path.join(test_data, 'keats')
print "keats=%s" % keats

class TopicTest(TestCase):
    
    def test_topics(self):
        topics = diagnidnif.mallet.topics(keats)
        self.assertEqual(topics, ["foo", "bar"])

