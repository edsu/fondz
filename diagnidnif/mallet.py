from os.path import join
import tempfile
import subprocess

from diagnidnif.utils import which

mallet = which('mallet')

def topics(source_dir, 
           num_topics=10, 
           num_top_words=15,
           num_threads=2, 
           iterations=1000, 
           doc_topics_threshold='0.1', 
           optimize_interval=10):

    tmp_dir = tempfile.mkdtemp()
    tmp_dir = 'foo'
    data_file = join(tmp_dir, 'data.mallet')
    state_file = join(tmp_dir, 'state.gz')
    topics_file = join(tmp_dir, 'topics.txt')
    topickeys_file = join(tmp_dir, 'topickeys.txt')

    subprocess.check_call([mallet, 'import-dir', 
        '--input', source_dir, 
        '--output', data_file, 
        '--keep-sequence',  
        '--remove-stopwords'])

    subprocess.check_call([mallet, 'train-topics',
        '--input', data_file,
        '--output-state', state_file, 
        '--num-topics', str(num_topics),
        '--num-threads', str(num_threads), 
        '--num-iterations', str(iterations),
        '--doc-topics-threshold', str(doc_topics_threshold), 
        '--optimize-interval', str(optimize_interval),
        '--num-top-words', str(num_top_words),
        '--output-doc-topics', topics_file,
        '--output-topic-keys', topickeys_file])
