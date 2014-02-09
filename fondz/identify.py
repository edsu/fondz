import csv
import logging

from utils import run, which, write_json
from os.path import abspath, join, relpath

fido = which("fido.py")

logger = logging.getLogger("fondz")


def get_file_formats(bag_dir):
    logger.info("starting format identification for %s", bag_dir)
    data_dir = join(abspath(bag_dir), "data")
    
    files = {}
    formats = {}

    rc, output = run([fido, "-r", data_dir])
    reader = csv.reader(output)
    for r in reader:
        puid, name, desc, path, mediatype = r[2], r[3], r[4], r[6], r[7]
        path = relpath(path, bag_dir)
        files[path] = puid
        formats[puid] = {
            "name": name,
            "description": desc,
            "mediatype": mediatype
        }
        logging.info("fido identified %s as %s", path, puid)

    logging.info("finished file identification for %s", bag_dir)

    return files, formats

