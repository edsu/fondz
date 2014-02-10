import json
import fondz
import shutil
import tempfile
import unittest

from os.path import join, dirname
from fondz.create import create
from fondz.utils import read_json
from fondz.topics import topics, summarize

bag = join(dirname(__file__), 'data', 'bag2')

class TopicTest(unittest.TestCase):
    
    def test_topics(self):
        fondz_dir = tempfile.mkdtemp()
        create(fondz_dir, bag, dir_exists=True)
        fondz_file = join(fondz_dir, 'js', 'fondz.json')
        fondz = read_json(fondz_file)
        results = fondz['topic_model']

        # make sure mallet details are present
        self.assertTrue('mallet' in results)
        self.assertEqual(len(results['mallet']), 2)

        # the actual topics 
        topics = results['topics']
        self.assertTrue(len(topics) > 0) 
        self.assertEqual(len(topics[0]['words']), 15)
        for topic in topics:
            self.assertTrue(len(topic['files']) > 0)
            self.assertTrue(len(topic['words']) > 0)
            self.assertTrue(topic['score'])
        shutil.rmtree(fondz_dir)

    def test_summarize(self): 
        # text_dir doesn't need to exist for this test, it is simply 
        # a test that the paths in the topics_file and made relative
        text_dir = '/home/ubuntu/fondz/x/derivatives'
        topics_file = join(dirname(__file__), 'data', 
                'topics.txt')
        topic_keys_file = join(dirname(__file__), 'data', 
                'topic_keys.txt')
        results = summarize(text_dir, topics_file, topic_keys_file, ['foo',
        'bar'], ['baz', 'bez'])

        self.assertEqual(results['mallet'][0], 'foo bar')
        self.assertEqual(results['mallet'][1], 'baz bez')

        t = results['topics'][0]
        self.assertEqual(t['words'], ['melancholy', 'thy', 'joy', 'hand',
            'soul', 'shade', 'sorrow', 'grape', 'beauty', 'hung', 'trophies',
            'cloudy', 'sadness', 'taste', 'fine'])
        self.assertEqual(t['files'], [
            ('2/keats-ode-495.txt.html', 0.662269496982198),
            ('1/keats-ode-495.txt.html', 0.6339728571559478)
        ])
