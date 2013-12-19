import os
import magic
import logging

from utils import run


get_mediatype = magic.Magic(mime=True)
get_description = magic.Magic()

def identify_dir(src_dir):
    src_dir = os.path.abspath(src_dir)
    parent_dir = os.path.dirname(src_dir)
    formats = []
    for dirpath, dirnames, filenames in os.walk(src_dir):
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(path, parent_dir)
            logging.info("format identification for %s", path)
            formats.append({
                "path": rel_path, 
                "mediatype": mediatype(path),
                "description": description(path),
                "encoding": encoding(path)
            })
    return formats

def mediatype(path):
    rc, stdout = run(['file', '-F', "\t", '--mime-type', path])
    if rc == 0:
        return stdout.read().split("\t")[1].strip()
    return None

def description(path):
    rc, stdout = run(['file', '-F', "\t", path])
    if rc == 0:
        return stdout.read().split("\t")[1].strip()
    return None

def encoding(path):
    rc, stdout = run(['file', '-F', "\t", '--mime-encoding', path])
    if rc == 0:
        return stdout.read().split("\t")[1].strip()
    return None
