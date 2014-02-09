import os
import re
import json
import time
import uuid
import fondz
import shutil
import logging
import datetime

from os.path import join, isdir, abspath, relpath
from fondz.topics import topics
from fondz.convert import convert
from fondz.identify import get_file_formats
from fondz.utils import render_to, write_json, read_json, template_dir


def create(fondz_dir, *bags, **kwargs):
    """
    create will initialize initialize a new fondz directory add one or more
    bags to it, convert what it can to web accessible formats, run topic 
    modeling, and format identification, and write out a HTML description
    """
    if not kwargs.get("dir_exists", False) and isdir(fondz_dir):
        raise Exception('fondz directory "%s" already exists' % fondz_dir)

    init(fondz_dir)

    # add all the bags
    for bag in bags:
        add_bag(fondz_dir, bag)

    # do topic modeling
    _add_topics(fondz_dir)

    # write the fondz description
    write(fondz_dir)


def init(fondz_dir):
    _mkdir(fondz_dir)
    _setup_logging(fondz_dir)
    
    logger = logging.getLogger("fondz")
    logger.info("created fondz %s", fondz_dir)

    _mkdir(fondz_dir, "derivatives")
    tmpl_dir = template_dir()
    shutil.copytree(join(tmpl_dir, "js"), join(fondz_dir, "js"))
    shutil.copytree(join(tmpl_dir, "css"), join(fondz_dir, "css"))
    shutil.copytree(join(tmpl_dir, "img"), join(fondz_dir, "img"))
    fondz_file = _fondz(fondz_dir)
    fondz = {
        "bags":[],
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
    fondz_file = _fondz(fondz_dir)
    fondz = read_json(fondz_file)
    for bag in fondz["bags"]:
        if bag["path"] == bag_dir:
            raise Exception("bag was already added: %s" % bag_dir)
    bag = _get_bag(bag_dir)
    _add_formats(bag, fondz)
    _convert(bag, fondz_dir)

    fondz["bags"].append(bag)
    fondz["bytes"] += bag["bytes"]
    fondz["num_files"] += len(bag["manifest"])

    write_json(fondz, fondz_file)


def write(fondz_dir):
    logger = logging.getLogger("fondz")
    logger.info("writing fondz description for %s", fondz_dir)

    index_file = join(fondz_dir, "index.html")
    fondz_file = _fondz(fondz_dir)
    fondz = read_json(fondz_file)
    format_summary = _summarize_formats(fondz)

    render_to('index.html', index_file, 
              fondz=fondz,
              format_summary=format_summary)


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
        cols = re.split(r' +', line, 1)
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


def _add_formats(bag, bags):
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
    fondz_file = _fondz(fondz_dir)
    fondz = read_json(fondz_file)
    fondz['topic_model'] = topics(fondz_dir)
    write_json(fondz, fondz_file)


def _fondz(fondz_dir):
    return join(fondz_dir, "js", "fondz.json")


def _mkdir(*parts):
    path = join(*parts)
    if not isdir(path):
        os.makedirs(path)

def _setup_logging(fondz_dir):
    logger = logging.getLogger("fondz")
    hdlr = logging.FileHandler(join(fondz_dir, "fondz.log"))
    formatter = logging.Formatter('%(asctime)-15s - %(levelname)s - %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

def _dt(t):
    return time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(int(t)))
