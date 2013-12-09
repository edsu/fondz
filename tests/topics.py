from unittest import TestCase

import 

class TopicTest(TestCase):
    
    def test_topics(self):
        topics = mallet()
        self.assertEqual(topics, ["cheese", "fondue"])

