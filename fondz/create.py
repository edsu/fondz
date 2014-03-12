import os
import re
import json
import time
import uuid
import fondz
import shutil
import logging
import datetime
import humanize

from os.path import join, isdir, abspath, relpath
from fondz.topics import topics
from fondz.convert import convert
from fondz.formats import get_file_formats
from fondz.utils import render_to, write_json, read_json, template_dir


def create(name, fondz_dir, *bags, **kwargs):
    """
    create will initialize initialize a new fondz directory add one or more
    bags to it, convert what it can to web accessible formats, run topic 
    modeling, and format identification, and write out a HTML description
    """
    if not kwargs.get("overwrite", False) and isdir(fondz_dir):
        raise Exception('fondz directory "%s" already exists' % fondz_dir)

    init(name, fondz_dir)

    # add all the bags
    for bag in bags:
        add_bag(fondz_dir, bag)

    # do topic modeling
    _add_topics(fondz_dir)

    # write the fondz description
    write(fondz_dir)


def init(name, fondz_dir):
    _mkdir(fondz_dir)
    _setup_logging(fondz_dir)
    
    logger = logging.getLogger("fondz")
    logger.info("created fondz %s", fondz_dir)

    _mkdir(fondz_dir, "derivatives")

    fondz_file = _fondz_file(fondz_dir)
    fondz = {
        "name": name,
        "bags": [],
        "bytes": 0,
        "num_files": 0,
        "formats": {}
    }
    write_json(fondz, fondz_file)



def add_bag(fondz_dir, bag_dir):
    """
    add a particular bagit directory to the fondz description
    """
    # TODO: validate bag first?
    logger = logging.getLogger("fondz")
    logger.info("adding bag %s to %s", bag_dir, fondz_dir)

    bag_dir = abspath(bag_dir)
    fondz_file = _fondz_file(fondz_dir)
    fondz = read_json(fondz_file)
    for bag in fondz["bags"]:
        if bag["path"] == bag_dir:
            raise Exception("bag was already added: %s" % bag_dir)
    bag = _get_bag(bag_dir)
    _add_formats(bag, fondz, fondz_dir)
    _convert(bag, fondz_dir)

    fondz["bags"].append(bag)
    fondz["bytes"] += bag["bytes"]
    fondz["num_files"] += len(bag["manifest"])

    write_json(fondz, fondz_file)


def write(fondz_dir):
    _setup_logging(fondz_dir)

    logger = logging.getLogger("fondz")
    logger.info("writing fondz description for %s", fondz_dir)

    fondz_file = _fondz_file(fondz_dir)
    fondz = read_json(fondz_file)

    _write_static(fondz_dir)
    _write_index_html(fondz_dir, fondz) 
    _write_topics_html(fondz_dir, fondz)
    _write_bags_html(fondz_dir, fondz)
    _write_formats_html(fondz_dir, fondz)

def _get_bag(path):
    bag = {
        "path": path, 
        "bytes": 0, 
        "info": {}, 
        "manifest": [],
        "id": uuid.uuid1().urn
    }
    # TODO: handle non-md5 manifests?
    manifest = join(path, "manifest-md5.txt")
    for line in open(manifest):
        line = line.strip()
        cols = re.split(r' +', line, maxsplit=1)
        path = join(bag['path'], cols[1])
        st = os.stat(path)
        rel_path = relpath(path, bag['path'])
        bag['bytes'] += st.st_size
        bag['manifest'].append({
            'path': rel_path,
            'bytes': st.st_size,
            'created': _dt(st.st_ctime),
            'modified': _dt(st.st_mtime),
            'md5': cols[0],
            'format': None
        })
    return bag


def _add_formats(bag, bags, fondz_dir):
    logger = logging.getLogger("fondz")
    logger.info("starting format identification for %s", fondz_dir)
    files, formats = get_file_formats(bag['path'])
    for f in bag['manifest']:
        f['format'] = files[f['path']]
    bags['formats'].update(formats)


def _convert(bag, fondz_dir):
    logger = logging.getLogger("fondz")
    logger.info("creating derivatives for %s", fondz_dir)
    source_dir = join(bag["path"], "data")
    target_dir = join(fondz_dir, "derivatives", bag['id'])
    convert(source_dir, target_dir)


def _summarize_formats(fondz):
    counts = {}
    for bag in fondz['bags']:
        for f in bag['manifest']:
            format_id = f['format']
            if format_id not in counts:
                counts[format_id] = []
            counts[format_id].append(f['path'])
    sorted_ids = counts.keys()
    sorted_ids.sort(lambda a, b: cmp(len(counts[b]), len(counts[a])))
    return [{'id': id, 'files': counts[id]} for id in sorted_ids]


def _add_topics(fondz_dir):
    logger = logging.getLogger("fondz")
    logger.info("doing topic modeling for %s", fondz_dir)
    fondz_file = _fondz_file(fondz_dir)
    fondz = read_json(fondz_file)
    fondz['topic_model'] = topics(fondz_dir)
    write_json(fondz, fondz_file)


def _fondz_file(fondz_dir):
    return join(fondz_dir, "fondz.json")


def _write_static(fondz_dir):
    tmpl_dir = template_dir()
    for dir_name in ["js", "css", "img"]:
        source_dir = join(tmpl_dir, dir_name)
        target_dir = join(fondz_dir, dir_name)
        if isdir(target_dir):
            shutil.rmtree(target_dir)
        shutil.copytree(source_dir, target_dir)


def _write_index_html(fondz_dir, fondz):
    index_file = join(fondz_dir, "index.html")
    format_summary = _summarize_formats(fondz)
    render_to('index.html', index_file, 
              fondz=fondz,
              humanize=humanize,
              format_summary=format_summary)
 

def _write_topics_html(fondz_dir, fondz):
    # write the overview
    topics_html = join(fondz_dir, "topics.html")
    render_to(
        'topics.html',
        topics_html, 
        fondz=fondz, 
        humanize=humanize
    )

    # write the topic specific files
    count = 0
    for topic in fondz['topic_model']['topics']:
        count += 1
        topic_file = join(fondz_dir, "topic-%02i.html" % count)
        render_to(
            'topic.html', 
            topic_file, 
            fondz=fondz, 
            topic=topic,
            count=0,
            humanize=humanize
        )


def _write_bags_html(fondz_dir, fondz):
    # write overview
    bags_html = join(fondz_dir, "bags.html")
    render_to('bags.html', bags_html, fondz=fondz, humanize=humanize)

    # and bag specific pages
    count = 0
    for bag in fondz['bags']:
        count += 1
        bag_html = join(fondz_dir, "bag-%05i.html" % count)
        render_to('bag.html', bag_html, fondz=fondz, bag=bag, humanize=humanize)


def _write_formats_html(fondz_dir, fondz):
    format_summary = _summarize_formats(fondz)
    formats_html = join(fondz_dir, "formats.html")
    render_to('formats.html', 
              formats_html, 
              fondz=fondz, 
              format_summary=format_summary,
              humanize=humanize)

    count = 0
    for format in format_summary:
        count += 1
        format_html = join(fondz_dir, "format-%03i.html" % count)
        render_to('format.html', format_html, fondz=fondz, format=format, 
                  humanize=humanize)


def _mkdir(*parts):
    path = join(*parts)
    if not isdir(path):
        os.makedirs(path)
    return path

def _setup_logging(fondz_dir):
    logger = logging.getLogger("fondz")
    hdlr = logging.FileHandler(join(fondz_dir, "fondz.log"))
    formatter = logging.Formatter('%(asctime)-15s - %(levelname)s - %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)

def _dt(t):
    return time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(int(t)))
