import shutil
import tempfile
from os.path import join, abspath

from utils import which, run, write_json

mallet = which('mallet')

def topics(fondz_dir, 
           num_topics=10, 
           num_top_words=15,
           num_threads=2, 
           iterations=1000, 
           doc_topics_threshold='0.1', 
           optimize_interval=10):
    """
    topics will do topic modeling on a fondz directory
    """

    if not mallet:
        raise Exception("mallet not found on PATH")

    text_dir = abspath(join(fondz_dir, "derivatives"))
    tmp_dir = tempfile.mkdtemp()
    data_file = join(tmp_dir, 'data.mallet')
    state_file = join(tmp_dir, 'state.gz')
    topics_file = join(tmp_dir, 'topics.txt')
    topic_keys_file = join(tmp_dir, 'topic_keys.txt')
    xml_topic_report = join(tmp_dir, 'report.xml')

    rc, stdout = run([mallet, 'import-dir', 
        '--input', text_dir, 
        '--output', data_file, 
        '--keep-sequence',  
        '--skip-html',
        '--remove-stopwords'])

    rc, stdout = run([mallet, 'train-topics',
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
    topics_json_file = join(fondz_dir, "js", "topics.json")
    write_json(results, topics_json_file)

    shutil.rmtree(tmp_dir)

    return results


def summarize(text_dir, topics_file, topic_keys_file):
    results = []

    # get the list of topics, and their scores
    for row in get_tsv(topic_keys_file):
        # need at least three columns: topic #, score and words
        if len(row) < 3: 
            continue
        t = {
            "words": row[2].split(" "), 
            "score": float(row[1]), 
            "files": []
        }
        results.append(t)

    # get the files and their associated topics
    for row in get_tsv(topics_file):
        # ignore header
        if len(row) == 1: continue

        doc_num = row.pop(0)
        doc = row.pop(0)
        doc = doc.replace('file:' + text_dir + '/', '') # make relative path
        files = []
        while len(row) > 0:
            topic_num = int(row.pop(0))
            proportion = float(row.pop(0))
            results[topic_num]['files'].append((doc, proportion))

    # sort the list of files for each topic descending by their proportion
    for t in results:
        t['files'].sort(lambda a, b: cmp(b[1], a[1]))

    # only include topics that are associated with files
    results = filter(lambda t: len(t['files']) > 0, results)

    return results
        

def get_tsv(filename):
    rows = []
    for line in open(filename):
        line = line.strip()
        rows.append(line.split("\t"))
    return  rows
