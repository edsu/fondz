import os
import magic
import logging

from utils import run


description = magic.Magic()
mediatype = magic.Magic(mime=True)
encoding = magic.Magic(mime_encoding=True)


def identify_dir(src_dir):
    logging.info("starting format identification for %s", src_dir)
    src_dir = os.path.abspath(src_dir)

    parent_dir = os.path.dirname(src_dir)
    formats = []
    for dirpath, dirnames, filenames in os.walk(src_dir, followlinks=True):
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(path, parent_dir)
            logging.info("format identification for %s", path)
            formats.append({
                "path": rel_path, 
                "mediatype": mediatype.from_file(path),
                "description": description.from_file(path),
                "encoding": encoding.from_file(path)
            })
    return formats
