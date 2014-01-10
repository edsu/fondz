import os
import json

from unittest import TestCase

from fondz.topics import topics, summarize

test_data = os.path.join(os.path.dirname(__file__), 'data', 'bag2', 'data')

class TopicTest(TestCase):
    
    def test_topics(self):
        results = topics(test_data)
        self.assertTrue(len(results), 10)
        self.assertEqual(len(results[0]['words']), 15)
        for topic in results:
            self.assertTrue(len(topic['files']) > 0)
            self.assertTrue(len(topic['words']) > 0)
            self.assertTrue(topic['score'])

    def test_summarize(self): 
        # text_dir doesn't need to exist for this test, it is simply 
        # a test that the paths in the topics_file and made relative
        text_dir = '/home/ubuntu/fondz/x/derivatives'
        topics_file = os.path.join(os.path.dirname(__file__), 'data', 
                'topics.txt')
        topic_keys_file = os.path.join(os.path.dirname(__file__), 'data', 
                'topic_keys.txt')
        results = summarize(text_dir, topics_file, topic_keys_file)

        t = results[0]
        self.assertEqual(t['words'], ['melancholy', 'thy', 'joy', 'hand',
            'soul', 'shade', 'sorrow', 'grape', 'beauty', 'hung', 'trophies',
            'cloudy', 'sadness', 'taste', 'fine'])
        self.assertEqual(t['files'], [
            ('2/keats-ode-495.txt.html', 0.662269496982198),
            ('1/keats-ode-495.txt.html', 0.6339728571559478)
        ])
