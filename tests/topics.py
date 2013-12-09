from unittest import TestCase

import diagnidnif

test_data = os.path.join(os.path.dirname(__name__), 'data')
keats = os.path.join(test_data, 'keats')

class TopicTest(TestCase):
    
    def test_topics(self):
        topics = diagnidnif.mallet.topics(keats)
        self.assertEqual(topics, ["foo", "bar"])

