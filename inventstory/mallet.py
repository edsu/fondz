import shutil
import tempfile
from os.path import join, abspath

from inventstory.utils import which, run

mallet = which('mallet')

def topics(text_dir, 
           num_topics=10, 
           num_top_words=15,
           num_threads=2, 
           iterations=1000, 
           doc_topics_threshold='0.1', 
           optimize_interval=10):

    text_dir = abspath(text_dir)
    tmp_dir = tempfile.mkdtemp()
    data_file = join(tmp_dir, 'data.mallet')
    state_file = join(tmp_dir, 'state.gz')
    topics_file = join(tmp_dir, 'topics.txt')
    topic_keys_file = join(tmp_dir, 'topic_keys.txt')
    xml_topic_report = join(tmp_dir, 'report.xml')

    run([mallet, 'import-dir', 
        '--input', text_dir, 
        '--output', data_file, 
        '--keep-sequence',  
        '--remove-stopwords'])

    run([mallet, 'train-topics',
        '--input', data_file,
        '--output-state', state_file, 
        '--num-topics', str(num_topics),
        '--num-threads', str(num_threads), 
        '--num-iterations', str(iterations),
        '--doc-topics-threshold', str(doc_topics_threshold), 
        '--optimize-interval', str(optimize_interval),
        '--num-top-words', str(num_top_words),
        '--output-doc-topics', topics_file,
        '--output-topic-keys', topic_keys_file])

    results = summarize(text_dir, topics_file, topic_keys_file)
    shutil.rmtree(tmp_dir)

    return results


def summarize(text_dir, topics_file, topic_keys_file):
    results = []

    # get the list of topics, and their scores
    for topic_key in get_tsv(topic_keys_file):
        t = {
            "words": topic_key[2].split(" "), 
            "score": float(topic_key[1]), 
            "files": []
        }
        results.append(t)

    # get the files and their associated topics
    for topic in get_tsv(topics_file):
        # ignore header
        if len(topic) == 1: continue

        doc_num = topic.pop(0)
        doc = topic.pop(0)
        doc = doc.replace('file:' + text_dir + '/', '') # make relative path
        files = []
        while len(topic) > 0:
            topic_num = int(topic.pop(0))
            proportion = float(topic.pop(0))
            results[topic_num]['files'].append((doc, proportion))

    # sort the list of files for each topic descending by their proportion
    for t in results:
        t['files'].sort(lambda a, b: cmp(b[1], a[1]))

    return results
        

def get_tsv(filename):
    rows = []
    for line in open(filename):
        line = line.strip()
        rows.append(line.split("\t"))
    return  rows
