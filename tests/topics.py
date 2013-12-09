from unittest import TestCase

import diagnidnif

class TopicTest(TestCase):
    
    def test_topics(self):
        topics = diagnidnif.mallet.topics()
        self.assertEqual(topics, ["foo", "bar"])

